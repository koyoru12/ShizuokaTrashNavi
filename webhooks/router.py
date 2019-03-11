import json

import tornado
from linebot.exceptions import (
    InvalidSignatureError
)

from webhooks import LineEventHandler, WebEventHandler


class LineRequestHandler(tornado.web.RequestHandler):
    """
    LINEからの直接のHttpリクエストを処理する。
    """
    def post(self):
        body = (self.request.body).decode('utf-8')
        signature = self.request.headers['X-Line-Signature']
        try:
            LineEventHandler.handle_request(body, signature)
        except InvalidSignatureError as e:
            print(e)
            self.send_error(400)

class WebRequestHandler(tornado.web.RequestHandler):
    """
    Webからのリクエストを処理する。
    """
    async def post(self):
        self.set_header('Access-Control-Allow-Origin', self.request.headers['origin'])
        body = (self.request.body).decode('utf-8')
        response = ''
        try:
            response = await WebEventHandler.handle_request(body)
        except Exception as e:
            print(e)
            self.send_error(400)
        self.write(json.dumps(response).encode())

