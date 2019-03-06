import util

class MessageFactory():
    message_dict = {}
    @classmethod
    def create_message(self, message_type):
        for key in self.message_dict:
            if key == message_type:
                return self.message_dict[key]()

    @classmethod
    def register_message(self, *message_class):
        for c in message_class:
            self.message_dict[c.message_type] = c

class AbstractMessage(util.JsonSerializable):
    pass

class HelpMessage(AbstractMessage):
    message_type = 'help'
    def __init__(self):
        self.body = 'このアプリの説明'
        self.type = self.message_type

class RequireLocationMessage(AbstractMessage):
    message_type = 'require_location'
    def __init__(self):
        self.body = 'どの地域の情報を知りたいですか？'
        self.type = self.message_type

MessageFactory.register_message(HelpMessage, RequireLocationMessage)