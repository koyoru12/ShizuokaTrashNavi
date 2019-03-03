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

line_bot_api = LineBotApi(str(os.environ.get('CHANNEL_ACCESS_TOKEN')))
handler = WebhookHandler(str(os.environ.get('CHANNEL_SECRET')))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    @gen.coroutine
    def fetch_api():
        http_client = httpclient.AsyncHTTPClient()
        http_req = httpclient.HTTPRequest(os.environ.get('API_GATEWAY'), method="POST")
        http_req.body = json.dumps({
            'name': 'アイロン'
        }).encode()
        res = yield http_client.fetch(http_req)
        res = res.body.decode('utf-8')

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=res)
        )
    fetch_api()

class LineApiHandler(tornado.web.RequestHandler):
    def post(self):
        body = (self.request.body).decode('utf-8')
        signature = self.request.headers['X-Line-Signature']
        try:
            handler.handle(body, signature)
        except InvalidSignatureError as e:
            print(e)
            self.send_error(400)
