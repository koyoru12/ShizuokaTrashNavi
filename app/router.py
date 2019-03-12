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

    def _send_response(self):
        self.write(self.response.to_json().encode())


class TextMessageRequestHandler(RequestHandler):
    def post(self):
        token = self.request.headers['Access-Token'] if 'Access-Token' in self.request.headers else ''
        if token != os.environ['API_APP_ACCESS_TOKEN']:
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
        body = json.loads(self.request.body)
        request_body = AddressMessageRequest(body)
        service = AddressMessageReplyService(request_body)
        for message in await service.try_register_address():
            self.response.append_message(message)
        """
        # unnamed loadとかで送られてくることもあるので注意
        pattern = '.+\d (...??[都道府県])(.+[市町村])'
        m = re.match(pattern, request_body.request_address)
        print(m.group(0))
        print(m.group(1))
        print(m.group(2))
        self.response.append_message(message)
        """
        self._send_response()
