import os
import re
import json
import logging

import tornado
from tornado import httpclient, gen
from tornado.ioloop import IOLoop

from app.services import TextMessageReplyService, AddressMessageReplyService, CityService, TokenProvider
from app.services.mail import send_mail
from app.models import MessageFactory, TextMessageRequest, AddressMessageRequest, Response


class RequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.response = Response()
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Authorization')

    def options(self):
        self.set_status(200)

    def _authenticate(self):
        token = self.request.headers['Access-Token'] if 'Access-Token' in self.request.headers else ''
        return False if token != os.environ['API_APP_ACCESS_TOKEN'] else True

    def _send_response(self):
        self.write(self.response.to_json().encode())


class TextMessageRequestHandler(RequestHandler):
    def post(self):
        if not self._authenticate():
            self.send_error(400)
        try:
            body = json.loads(self.request.body)
            request_body = TextMessageRequest(body)

            service = TextMessageReplyService(request_body)
            messages = service.reply()
            for message in messages:
                self.response.append_message(message)
            self._send_response()
        except Exception as e:
            logging.error(e)
            self.send_error(400)        


class AddressMessageRequestHandler(RequestHandler):
    async def post(self):
        if not self._authenticate():
            self.send_error(400)
        body = json.loads(self.request.body)
        request_body = AddressMessageRequest(body)
        service = AddressMessageReplyService(request_body)
        for message in await service.try_register_address():
            self.response.append_message(message)
        self._send_response()


class GetValidCityHandler(RequestHandler):
    def get(self):
        rows = CityService.get_all_city()
        city_list = [{'name':city['city_name'], 'id':city['id']} for city in rows]
        self.write(json.dumps(city_list).encode())


class LineTokenAuthenticationHandler(RequestHandler):
    """トークンを検証する
    """
    def get(self):
        try:
            token = self.request.headers['Authorization']
            result = TokenProvider.authenticate(token)
            if not result:
                self.send_error(400)
            self.set_status(200)
        except Exception as e:
            logging.error(e)
            self.send_error(400)


class ChangeUserCityHandler(RequestHandler):
    """ユーザの登録市町村を変更する
    """
    def post(self):
        try:
            token = self.request.headers['Authorization']
            user_id = TokenProvider.authenticate(token)
            city_id = self.request.body.decode()
            if not user_id:
                self.send_error(400)
        except Exception as e:
            logging.error(e)
            self.send_error(400)
        self.set_status(200)
        CityService.register_user_city(user_id, city_id)


class ContactHandler(RequestHandler):
    """メールフォームのエンドポイント
    """
    async def post(self):
        try:
            content = json.loads(self.request.body.decode())
            await IOLoop.current().run_in_executor(None, send_mail, content)
            self.set_status(200)
        except Exception as e:
            logging.error(e)
            self.send_error(400)