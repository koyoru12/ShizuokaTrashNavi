import util


class TextMessageRequest(util.JsonSerializable):
    def __init__(self, request_body):
        request_body['config'] = request_body['config'] if 'config' in request_body else {}

        self.user_id = request_body['user_id']
        self.request_message = request_body['request_message']
        self.client = request_body['client']
        self.config = TextMessageConfig(request_body['config'])
        self.action = TextMessageAction(request_body['action'])

class TextMessageConfig(util.JsonSerializable):
    def __init__(self, config):
        # 検索市町村の指定
        self.search_city = config['search_city'] if 'search_city' in config else ''

class TextMessageAction(util.JsonSerializable):
    def __init__(self, action):
        self.type = action['type'] if 'type' in action else ''
        self.query = action['query'] if 'query' in action else '' 

class AddressMessageRequest(util.JsonSerializable):
    def __init__(self, request_body):
        self.user_id = request_body['user_id']
        self.longitude = request_body['longitude']
        self.latitude = request_body['latitude']
    