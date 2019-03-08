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

    @classmethod
    def initialize(self):
        self.line_client = LineBotApi(str(os.environ.get('CHANNEL_ACCESS_TOKEN')))
        self.line_handler = WebhookHandler(str(os.environ.get('CHANNEL_SECRET')))

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
                raw_response = yield http_client.fetch(http_req)
                self.handle_response(event, raw_response)
            requestasync()

        @self.line_handler.add(MessageEvent, message=LocationMessage)
        def handle_message(event):
            url = os.environ.get('API_APP_ADDRESS')
            body = {
                'request_address': event.message.address,
                'user_id': event.source.user_id
            }
            @gen.coroutine
            def requestasync():
                http_client = httpclient.AsyncHTTPClient()
                http_req = httpclient.HTTPRequest(url, method='POST')
                http_req.body = json.dumps(body).encode()
                raw_response = yield http_client.fetch(http_req)
                self.handle_response(event, raw_response)
            requestasync()

    @classmethod
    def handle_request(self, body, signature):
        self.line_handler.handle(body, signature)

    @classmethod
    def handle_response(self, event, raw_response):
        raw_body = raw_response.body.decode('utf-8')
        response = json.loads(raw_body)
        reply = []
        for index, message in enumerate(response['messages']):
            reply.append(ResponseFactory.create_response(message))
        self.line_client.reply_message(
            event.reply_token,
            reply
        )

