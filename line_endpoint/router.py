import os
import json
import tornado
from tornado import httpclient, web, concurrent, gen
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_client = LineBotApi(str(os.environ.get('CHANNEL_ACCESS_TOKEN')))
line_handler = WebhookHandler(str(os.environ.get('CHANNEL_SECRET')))

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    url = os.environ.get('API_APP_GATEWAY')
    body = {
        'request_message': event.message.text
    }
    @gen.coroutine
    def requestasync():
        http_client = httpclient.AsyncHTTPClient()
        http_req = httpclient.HTTPRequest(url, method='POST')
        http_req.body = json.dumps(body).encode()
        res = yield http_client.fetch(http_req)
        res_body = res.body.decode('utf-8')
        line_client.reply_message(
            event.reply_token,
            TextSendMessage(text=res_body)
        )
    requestasync()

class LineWebRequestHandler(tornado.web.RequestHandler):
    """
    LINEからの直接のHttpリクエストを処理する。
    """
    def post(self):
        body = (self.request.body).decode('utf-8')
        signature = self.request.headers['X-Line-Signature']
        try:
            self._fetch_response_message(body, signature)
#            LineEventHandler.handle(body, signature)
        except InvalidSignatureError as e:
            print(e)
            self.send_error(400)

    def _fetch_response_message(self, body, signature):
        line_handler.handle(body, signature)
