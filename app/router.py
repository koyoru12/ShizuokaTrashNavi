import os
import re
import json
import tornado
from tornado import httpclient, gen
from app.reply import DynamicReplyHandler, FixedReplyHandler
from app.user import Users
from app.models import MessageFactory, TextMessageRequest, AddressMessageRequest, Response

class RequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.response = Response()

    def _send_response(self):
        self.write(self.response.to_json().encode())


class TextMessageRequestHandler(RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        request_body = TextMessageRequest(body)
        message = FixedReplyHandler.handle(request_body)
        if message is not None:
            self.response.append_message(message)
            self._send_response()
            return

        # 定型メッセージで処理できなかった場合
        
        user_id = body['user_id']
        res = Users.fetch(user_id)
        if res is None:
            message = MessageFactory.create_message('require_address', request_body)
            self.response.append_message(message)

        message = DynamicReplyHandler.handle(request_body)
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
        message = MessageFactory.create_message('response_address', request_body)
        self.response.append_message(message)
        self._send_response()
