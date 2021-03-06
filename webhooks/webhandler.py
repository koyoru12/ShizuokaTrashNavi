import os
import json

import tornado
from tornado import httpclient

from webhooks.models.response import ResponseFactory
from app.models import TextMessageRequest

class WebEventHandler():
    @classmethod
    async def handle_request(self, body):
        body = json.loads(body)
        body['client'] = 'web'
        body['user_id'] = ''
        request = TextMessageRequest(body)
        url = os.environ.get('API_APP_MESSAGE')
        http_client = httpclient.AsyncHTTPClient()
        http_req = httpclient.HTTPRequest(url, method='POST')
        http_req.headers = {'Access-Token': os.environ['API_APP_ACCESS_TOKEN']}
        http_req.body = json.dumps(body).encode()
        raw_response = await http_client.fetch(http_req)
        return self.handle_response(raw_response)
    
    @classmethod
    def handle_response(self, raw_response):
        raw_body = raw_response.body.decode('utf-8')
        response = json.loads(raw_body)
        reply = []
        for index, message in enumerate(response['messages']):
            mes = ResponseFactory.create_response(message)
            reply.append(mes.as_json_dict())
        return reply