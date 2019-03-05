import json
import tornado

class FixedResponseHandler():
    @classmethod
    def handle(self, message):
        response = {
            'resolve': False,
            'message_type': '',
            'message_body': ''
        }
        if (message == 'ヘルプ'):
            response['message_type'] = 'help'
            response['message_body'] = '静岡県のごみ分別botです！'
            response['resolve'] = True
        return response