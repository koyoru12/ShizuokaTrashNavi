from linebot.models import (
    TextSendMessage, FlexSendMessage,
    TextMessage, LocationMessage, 
    QuickReply, QuickReplyButton,
    BubbleContainer, BoxComponent, TextComponent, SeparatorComponent,
    LocationAction, MessageAction
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


class ThanksResponse(AbstractResponse):
    message_type = 'thanks'
    def create_response(self):
        return TextSendMessage(text=self._context['body'])


class MistakeResponse(AbstractResponse):
    message_type = 'mistake'
    def create_response(self):
        return TextSendMessage(text=self._context['body'])


class RequireAddressResponse(AbstractResponse):
    message_type = 'require_address'
    def create_response(self):
        return TextSendMessage(text=self._context['body']['line'],
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
            contents = [
                TextComponent(
                    text=self._context['body'],
                    wrap=True,
                    size='sm'
                ),
                SeparatorComponent(),
            ]
            if trashinfo['name'] != '':
                contents.append(TextComponent(text='名前', color='#a0a0a0', size='sm'))
                contents.append(TextComponent(text=trashinfo['name'], wrap=True, size='sm'))
            if trashinfo['category'] != '':
                contents.append(TextComponent(text='種類', color='#a0a0a0', size='sm'))
                contents.append(TextComponent(text=trashinfo['category'], wrap=True,  size='sm'))
            if trashinfo['note'] != '':
                contents.append(TextComponent(text='メモ', color='#a0a0a0', size='sm'))
                contents.append(TextComponent(text=trashinfo['note'], wrap=True, size='sm'))

        return FlexSendMessage(
            alt_text=self._context['body'],
            contents = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=contents,
                    spacing='md'
                )
            )
        )


class TrashSelectResponse(AbstractResponse):
    message_type = 'trash_select'
    def create_response(self):
        contents = [
            TextComponent(
                text=self._context['body'],
                wrap=True,
                size='sm'
            ),
            SeparatorComponent()
        ]
        for index, name in enumerate(self._context['trash_list']):
            contents.append(TextComponent(
                text=name,
                color='#0000ff',
                wrap=True,
                action=MessageAction(text=name)
            ))
        return FlexSendMessage(
            alt_text=self._context['body'],
            contents = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=contents,
                    spacing='md'
                )
            )
        )


class ResponseAddressSuccessResponse(AbstractResponse):
    message_type = 'response_address_success'
    def create_response(self):
        return TextSendMessage(text=self._context['body'])


class ResponseAddressRejectResponse(AbstractResponse):
    message_type = 'response_address_reject'
    def create_response(self):
        return TextSendMessage(text=self._context['body'])



ResponseFactory.register_response(
    HelpResponse, ThanksResponse, MistakeResponse,
    RequireAddressResponse, ResponseAddressSuccessResponse,
    ResponseAddressRejectResponse, TrashInfoResponse, TrashSelectResponse)