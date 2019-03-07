import util


class MessageFactory():
    """MessageFactory
    """

    message_dict = {}

    @classmethod
    def create_message(self, message_type, context):
        for key in self.message_dict:
            if key == message_type:
                return self.message_dict[key](context)
        raise Exception('Type not found > ' + message_type)

    @classmethod
    def register_message(self, *message_class):
        for c in message_class:
            self.message_dict[c.message_type] = c


class AbstractMessage(util.JsonSerializable):
    """AbstractMessage
    """

    def __init__(self, context):
        self._context = context


class HelpMessage(AbstractMessage):
    """HelpMessage
    """

    message_type = 'help'
    def __init__(self, context):
        super().__init__(context)
        self.body = 'このアプリの説明'
        self.type = self.message_type


class RequireAddressMessage(AbstractMessage):
    """RequireAddressMessage
    """

    message_type = 'require_address'
    def __init__(self, context):
        super().__init__(context)
        self.body = 'どの地域の情報を知りたいですか？'
        self.type = self.message_type


class ResponseAddressMessage(AbstractMessage):
    """ResponseAddressMessage
    """

    message_type = 'response_address'
    def __init__(self, context):
        super().__init__(context)
        self.body = '地域情報を登録しました！'
        self.type = self.message_type


class TrashInfoMessage(AbstractMessage):
    """TrashMessage
    """

    message_type = 'trash_info'
    def __init__(self, context):
        super().__init__(context)
        self.body = 'ごみに関する情報です'
        self.type = self.message_type
        self.trash_info = []
    
    def append_trash_info(self, trash_info):
        if trash_info == None:
            self.body = 'ごめんなさい。情報が見つかりませんでした。'
        self.trash_info = trash_info
    

MessageFactory.register_message(HelpMessage, RequireAddressMessage, ResponseAddressMessage, TrashInfoMessage)