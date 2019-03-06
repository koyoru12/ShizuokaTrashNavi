import os
import json
import tornado
from tornado import httpclient, gen
from app.response import DynamicResponseHandler, FixedResponseHandler
from app.user import Users
from app.models import MessageFactory

class TextMessageRequestHandler(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        request_message = body['request_message']
        res = FixedResponseHandler.handle(request_message)
        if (res.resolve):
            self.write(res.message.to_json().encode())
            return

        # 定型メッセージで処理できなかった場合
        
        # fix:
        user_id = body['user_id']
        res = Users.fetch(user_id)
        if res is None:
            message = MessageFactory.create_message('require_location')
            self.write(message.to_json().encode())
            return

        res = DynamicResponseHandler.handle(request_message)
        self.write(json.dumps(res, ensure_ascii=False).encode())

class AddressMessageRequestHandler(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        print(body)
        self.write('ok')