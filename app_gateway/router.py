import os
import json
import tornado
from tornado import httpclient, gen
from app_gateway.fixed_response import FixedResponseHandler
from app_gateway.trashdb import TrashDbHandler

class AppGatewayHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        body = json.loads(self.request.body)
        request_message = body['request_message']
        res = FixedResponseHandler.handle(request_message)
        if (res['resolve']):
            self.write(json.dumps(res, ensure_ascii=False).encode())

        # 定型メッセージで処理できなかった場合
        # TrashDBを検索する
        res = TrashDbHandler.handle(request_message)
        self.write(json.dumps(res, ensure_ascii=False).encode())
