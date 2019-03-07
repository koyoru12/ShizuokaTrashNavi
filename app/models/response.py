import util

class Response(util.JsonSerializable):
    def __init__(self):
        self.messages = []
    
    def append_message(self, message):
        self.messages.append(message)
    
    def message_length(self):
        return len(self.messages)