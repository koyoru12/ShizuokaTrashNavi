from linebot.models import (
    TextSendMessage,
    TextMessage, LocationMessage,
    QuickReply, QuickReplyButton,
    LocationAction
)


class ResponseFactory():

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

    def __init__(self, context):
        self._context = context


class HelpResponse(AbstractResponse):

    message_type = 'help'
    def create_response(self):
        return TextSendMessage(text=self._context['body'])


class RequireAddressResponse(AbstractResponse):

    message_type = 'require_address'
    def create_response(self):
        return TextSendMessage(text=self._context['body'],
                        quick_reply=QuickReply(items=[
                            QuickReplyButton(action=LocationAction(label='location'))
                        ]))

class TrashInfoResponse(AbstractResponse):

    message_type = 'trash_info'
    def create_response(self):
        if len(self._context['trash_info']) == 0:
            return TextSendMessage(text=self._context['body'])
        else:
            trashinfo = self._context['trash_info'][0]
            message = (
            '{head}\n'
            '-----------------------------------\n'
            '名前: {name}\n'
            '種類: {category}\n'
            '備考: {note}'
            ).format(head=self._context['body'], name=trashinfo['name'],
                     category=trashinfo['category'], note=trashinfo['note'])
#            message = self._context['body'] + '\n' + trashinfo['name']
            return TextSendMessage(text=message)


class ResponseAddressSuccessResponse(AbstractResponse):

    message_type = 'response_address_success'
    def create_response(self):
        return TextSendMessage(text=self._context['body'])


class ResponseAddressRejectResponse(AbstractResponse):

    message_type = 'response_address_reject'
    def create_response(self):
        return TextSendMessage(text=self._context['body'])



ResponseFactory.register_response(
    HelpResponse, RequireAddressResponse, ResponseAddressSuccessResponse,
    ResponseAddressRejectResponse, TrashInfoResponse)