import os
import json

from tornado import httpclient, gen
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, LocationMessage
)

from line.models.response import ResponseFactory


class LineEventHandler():
    """LineEventHandler
    """

    line_client = LineBotApi(str(os.environ.get('CHANNEL_ACCESS_TOKEN')))
    line_handler = WebhookHandler(str(os.environ.get('CHANNEL_SECRET')))

    @classmethod
    def init(self):
        @self.line_handler.add(MessageEvent, message=TextMessage)
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
                self.line_client.reply_message(
                    event.reply_token,
                    response
                )
            requestasync()

        @self.line_handler.add(MessageEvent, message=LocationMessage)
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
                self.line_client.reply_message(
                    event.reply_token,
                    response
                )
            requestasync()

    @classmethod
    def handle(self, body, signature):
        self.line_handler.handle(body, signature)