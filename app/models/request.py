import util


class TextMessageRequest(util.JsonSerializable):
    def __init__(self, request_body):
        self.user_id = request_body['user_id']
        self.request_message = request_body['request_message']


class AddressMessageRequest(util.JsonSerializable):
    def __init__(self, request_body):
        self.user_id = request_body['user_id']
        self.request_address = request_body['request_address']
    