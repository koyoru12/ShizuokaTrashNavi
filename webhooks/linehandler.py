import os
import json
import datetime

import jwt
from tornado import httpclient, gen
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, PostbackEvent,
    TextMessage, LocationMessage
)

from webhooks.models.response import ResponseFactory


class LineEventHandler():

    @classmethod
    def initialize(self):
        self.line_client = LineBotApi(str(os.environ.get('CHANNEL_ACCESS_TOKEN')))
        self.line_handler = WebhookHandler(str(os.environ.get('CHANNEL_SECRET')))

        # テキストメッセージハンドラ
        @self.line_handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            url = os.environ.get('API_APP_MESSAGE')
            body = {
                'request_message': event.message.text,
                'user_id': event.source.user_id,
                'client': 'line',
                'config': {},
                'action': ''
            }
            @gen.coroutine
            def requestasync():
                http_client = httpclient.AsyncHTTPClient()
                http_req = httpclient.HTTPRequest(url, method='POST')
                http_req.headers = {'Access-Token': os.environ['API_APP_ACCESS_TOKEN']}
                http_req.body = json.dumps(body).encode()
                raw_response = yield http_client.fetch(http_req)
                self.handle_response(event, raw_response)
            requestasync()

        # ポストバックアクションハンドラ
        @self.line_handler.add(PostbackEvent)
        def handle_message(event):
            print('hook')
            url = os.environ.get('API_APP_MESSAGE')
            body = {
                'request_message': '',
                'user_id': event.source.user_id,
                'client': 'line',
                'config': {},
                'action': event.postback.data
            }
            @gen.coroutine
            def requestasync():
                http_client = httpclient.AsyncHTTPClient()
                http_req = httpclient.HTTPRequest(url, method='POST')
                http_req.headers = {'Access-Token': os.environ['API_APP_ACCESS_TOKEN']}
                http_req.body = json.dumps(body).encode()
                raw_response = yield http_client.fetch(http_req)
                self.handle_response(event, raw_response)
            requestasync()

        # 位置情報メッセージハンドラ
        @self.line_handler.add(MessageEvent, message=LocationMessage)
        def handle_message(event):
            url = os.environ.get('API_APP_ADDRESS')
            body = {
                'user_id': event.source.user_id,
                'longitude': event.message.longitude,
                'latitude': event.message.latitude
            }
            @gen.coroutine
            def requestasync():
                http_client = httpclient.AsyncHTTPClient()
                http_req = httpclient.HTTPRequest(url, method='POST')
                http_req.headers = {'Access-Token': os.environ['API_APP_ACCESS_TOKEN']}
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
            mes = ResponseFactory.create_response(message)
            reply.append(mes)
        self.line_client.reply_message(
            event.reply_token,
            reply
        )


class TokenProvider:
    secret_key = os.environ['TOKEN_SECRET']
    
    @classmethod
    def issue(self, user_id):
        """認証トークンを発行する
        """
        encoded = jwt.encode({
            'user_id': user_id,
            'iat': datetime.datetime.now(),
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
        }, self.secret_key)
        return encoded

    @classmethod
    def authenticate(token):
        try:
            decoded = jwt.decode(encoded, key)
            return decoded['user_id']
        except Exception:
            return False