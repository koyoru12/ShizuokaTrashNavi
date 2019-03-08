import util


class MessageFactory():

    message_dict = {}

    @classmethod
    def create_message(self, message_type, context, **kwargs):
        for key in self.message_dict:
            if key == message_type:
                return self.message_dict[key](context, **kwargs)
        raise Exception('Type not found > ' + message_type)

    @classmethod
    def register_message(self, *message_class):
        for c in message_class:
            self.message_dict[c.message_type] = c


class AbstractMessage(util.JsonSerializable):

    def __init__(self, context):
        self._context = context


class HelpMessage(AbstractMessage):

    message_type = 'help'
    def __init__(self, context):
        super().__init__(context)
        self.body = 'このアプリの説明'
        self.type = self.message_type


class RequireAddressMessage(AbstractMessage):

    message_type = 'require_address'
    def __init__(self, context):
        super().__init__(context)
        self.body = {
            'line': 'まだ地域を登録していないみたいですね。\n'
                    + '下のボタンをタップしてお住まいの地域を教えてください！✨\n'
                    + '分別情報をお住まいの地域で検索できるかも知れませんよ😉'
        }
        self.type = self.message_type


class ResponseAddressSuccessMessage(AbstractMessage):

    message_type = 'response_address_success'
    def __init__(self, context, city_name):
        super().__init__(context)
        self.body = '地域を登録しました！✨\n次から{}でごみ分別情報を検索しますね😉'.format(city_name)
        self.type = self.message_type


class ResponseAddressRejectMessage(AbstractMessage):

    message_type = 'response_address_reject'
    def __init__(self, context):
        super().__init__(context)
        # FIX:
        # 登録できる市町村の案内
        self.body = 'ごめんなさい〜！😣\nその市町村には対応していないんです…。'
        self.type = self.message_type


class TrashInfoMessage(AbstractMessage):

    message_type = 'trash_info'
    def __init__(self, context):
        super().__init__(context)
        self.body = ''
        self.type = self.message_type
        self.trash_info = []
    
    def append_trash_info(self, trash_info):
        if trash_info == None:
            self.body = 'ごめんなさい〜！😣\n情報が見つかりませんでした…。'
        else:
            trash_dict = {}
            self.body = trash_info['city_name'] + 'の情報です。お探しの情報はこちらですか？'
            for key in trash_info.keys():
                trash_dict[key] = trash_info[key]
            self.trash_info.append(trash_dict)

MessageFactory.register_message(
    HelpMessage, RequireAddressMessage, ResponseAddressSuccessMessage,
    ResponseAddressRejectMessage, TrashInfoMessage)