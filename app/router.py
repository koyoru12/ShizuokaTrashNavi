import os
import re
import json
import tornado
from tornado import httpclient, gen
from app.reply import DynamicReplyHandler, FixedReplyHandler
from app.models import MessageFactory, TextMessageRequest, AddressMessageRequest, Response
from app.db import City, User

class RequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.response = Response()

    def _send_response(self):
        self.write(self.response.to_json().encode())


class TextMessageRequestHandler(RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        request_body = TextMessageRequest(body)

        # 定型メッセージでの処理を試みる
        handler = FixedReplyHandler(request_body)
        for message in handler.handle():
            self.response.append_message(message)
        if (self.response.message_length() > 0):
            self._send_response()
            return

        # 定型メッセージで処理できない場合は動的メッセージで処理する
        handler = DynamicReplyHandler(request_body)
        for message in handler.handle():
            self.response.append_message(message)
        self._send_response()

        

class AddressMessageRequestHandler(RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        request_body = AddressMessageRequest(body)
        # unnamed loadとかで送られてくることもあるので注意
        pattern = '.+\d (...??[都道府県])(.+[市町村])'
        m = re.match(pattern, request_body.request_address)
        print(m.group(0))
        print(m.group(1))
        print(m.group(2))
        city = City.fetch(m.group(2))
        if city is None:
            # リクエストされた市町村に対応していない場合
            message = MessageFactory.create_message('response_address_reject', request_body)
        else:
            # 市町村情報を登録
            if User.fetch(request_body.user_id) is None:
                # ユーザ登録がない場合は登録
                User.register(request_body.user_id, city['id'])
            else:
                # ユーザ登録がある場合は更新
                User.update(request_body.user_id, city['id'])
            message = MessageFactory.create_message('response_address_success', request_body)
        self.response.append_message(message)
        self._send_response()
