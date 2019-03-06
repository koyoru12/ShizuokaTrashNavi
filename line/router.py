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
#            self._fetch_response_message(body, signature)
            LineEventHandler.handle(body, signature)
        except InvalidSignatureError as e:
            print(e)
            self.send_error(400)

    def _fetch_response_message(self, body, signature):
        line_handler.handle(body, signature)
