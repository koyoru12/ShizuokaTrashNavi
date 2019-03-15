import os
import re
import json

import tornado
from tornado import httpclient, gen

from app.services import TextMessageReplyService, AddressMessageReplyService
from app.models import MessageFactory, TextMessageRequest, AddressMessageRequest, Response


class RequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.response = Response()

    def _authenticate(self):
        token = self.request.headers['Access-Token'] if 'Access-Token' in self.request.headers else ''
        return False if token != os.environ['API_APP_ACCESS_TOKEN'] else True

    def _send_response(self):
        self.write(self.response.to_json().encode())


class TextMessageRequestHandler(RequestHandler):
    def post(self):
        if not self._authenticate():
            self.send_error(400)
        body = json.loads(self.request.body)
        request_body = TextMessageRequest(body)

        service = TextMessageReplyService(request_body)
        messages = service.reply()
        for message in messages:
            self.response.append_message(message)
        self._send_response()
        

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


class GetValidCityHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Access-Control-Allow-Origin', self.request.headers['origin'])
        city = [
            {
                'name': '静岡市',
                'id': 'a'
            },
            {
                'name': '浜松市',
                'id': 'a'
            }
        ]
        self.write(json.dumps(city).encode())