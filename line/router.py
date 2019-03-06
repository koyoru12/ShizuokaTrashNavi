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
    MessageEvent, TextMessage, LocationMessage, QuickReply, QuickReplyButton, TextSendMessage,
    LocationAction
)

from line.models.response import ResponseFactory

line_client = LineBotApi(str(os.environ.get('CHANNEL_ACCESS_TOKEN')))
line_handler = WebhookHandler(str(os.environ.get('CHANNEL_SECRET')))

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    url = os.environ.get('API_APP_MESSAGE')
    body = {
        'request_message': event.message.text,
        'user_id': event.source.user_id
    }
    @gen.coroutine
    def requestasync():
        http_client = httpclient.AsyncHTTPClient()
        http_req = httpclient.HTTPRequest(url, method='POST')
        http_req.body = json.dumps(body).encode()
        res = yield http_client.fetch(http_req)
        res_body = res.body.decode('utf-8')
        response = ResponseFactory.create_response(json.loads(res_body))
        line_client.reply_message(
            event.reply_token,
            response
        )
    requestasync()

@line_handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    url = os.environ.get('API_APP_ADDRESS')
    body = {
        'request_location': event.message.address,
        'user_id': event.source.user_id
    }
    @gen.coroutine
    def requestasync():
        http_client = httpclient.AsyncHTTPClient()
        http_req = httpclient.HTTPRequest(url, method='POST')
        http_req.body = json.dumps(body).encode()
        res = yield http_client.fetch(http_req)
        res_body = res.body.decode('utf-8')
        response = ResponseFactory.create_response(json.loads(res_body))
        line_client.reply_message(
            event.reply_token,
            response
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
