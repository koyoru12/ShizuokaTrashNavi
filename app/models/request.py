import util
import urllib


class TextMessageRequest(util.JsonSerializable):
    def __init__(self, request_body):
        request_body['config'] = request_body['config'] if 'config' in request_body else {}

        self.user_id = request_body['user_id'] if 'user_id' in request_body else ''
        self.request_message = request_body['request_message'] if 'request_message' in request_body else ''
        self.client = request_body['client'] if 'client' in request_body else ''
        self.config = TextMessageConfig(request_body['config'])
        self.action = TextMessageAction(request_body['action'])


class TextMessageConfig(util.JsonSerializable):
    def __init__(self, config):
        # 検索市町村の指定
        self.search_cityid = config['search_cityid'] if 'search_cityid' in config else ''

class TextMessageAction(util.JsonSerializable):
    def __init__(self, action):
        self.type = ''
        act_dic = urllib.parse.parse_qs(action)
        for key in act_dic:
            setattr(self, key, act_dic[key][0])


class AddressMessageRequest(util.JsonSerializable):
    def __init__(self, request_body):
        self.user_id = request_body['user_id']
        self.longitude = request_body['longitude']
        self.latitude = request_body['latitude']
    