import tornado
from tornado import httpclient, web, concurrent, gen

from linebot.exceptions import (
    InvalidSignatureError
)

from line import LineEventHandler


class LineWebRequestHandler(tornado.web.RequestHandler):
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

