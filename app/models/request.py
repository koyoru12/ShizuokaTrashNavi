import util


class TextMessageRequest(util.JsonSerializable):
    def __init__(self, request_body):
        self.user_id = request_body['user_id']
        self.request_message = request_body['request_message']


class AddressMessageRequest(util.JsonSerializable):
    def __init__(self, request_body):
        self.user_id = request_body['user_id']
        self.longitude = request_body['longitude']
        self.latitude = request_body['latitude']
    