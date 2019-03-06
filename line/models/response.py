from linebot.models import (
    TextSendMessage,
    TextMessage, LocationMessage,
    QuickReply, QuickReplyButton,
    LocationAction
)


class ResponseFactory():
    """ResponseFactory
    """

    response_builder_dict = {}
    @classmethod
    def create_response(self, context):
        print(context)
        for key in self.response_builder_dict:
            if key == context['type']:
                builder = self.response_builder_dict[key](context)
                return builder.create_response()
        raise Exception('Type not found > ' + context['type'])

    @classmethod
    def register_response(self, *message_class):
        for c in message_class:
            self.response_builder_dict[c.message_type] = c


class AbstractResponse():
    """AbstractResponse
    """

    def __init__(self, context):
        self._context = context


class HelpResponse(AbstractResponse):
    """HelpResponse
    """

    message_type = 'help'
    def create_response(self):
        return TextSendMessage(text=self._context['body'])


class RequireLocationResponse(AbstractResponse):
    """RequireLocationResponse
    """

    message_type = 'require_location'
    def create_response(self):
        return TextSendMessage(text=self._context['body'],
                        quick_reply=QuickReply(items=[
                            QuickReplyButton(action=LocationAction(label='location'))
                        ])),

ResponseFactory.register_response(HelpResponse, RequireLocationResponse)