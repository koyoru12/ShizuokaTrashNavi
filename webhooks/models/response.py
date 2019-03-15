from linebot.models import (
    TextSendMessage, FlexSendMessage,
    TextMessage, LocationMessage, 
    QuickReply, QuickReplyButton,
    BubbleContainer, BoxComponent, TextComponent, SeparatorComponent, ButtonComponent,
    LocationAction, MessageAction, PostbackAction, URIAction
)

Colors = {
    'primary': '#3469E6',
    'link': '#0000FF'
}    

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
        contents = [
            TextComponent(
                text=self._context['text'],
                wrap=True,
                size='sm'
            ),
            SeparatorComponent()
        ]
        for index, content in enumerate(self._context['contents']):
            contents.append(TextComponent(
                text=content['text'],
                color=Colors['link'],
                wrap=True,
                action=PostbackAction(data=content['postback'], display_text=content['text'])
            ))
        return FlexSendMessage(
            alt_text=self._context['text'],
            contents = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=contents,
                    spacing='md'
                )
            )
        )
        return TextSendMessage(text=self._context['text'])


class ThanksResponse(AbstractResponse):
    message_type = 'thanks'
    def create_response(self):
        return TextSendMessage(text=self._context['text'])


class MistakeResponse(AbstractResponse):
    message_type = 'mistake'
    def create_response(self):
        return TextSendMessage(text=self._context['text'])


class RequireAddressResponse(AbstractResponse):
    message_type = 'require_address'
    def create_response(self):
        return TextSendMessage(text=self._context['text']['line'],
                        quick_reply=QuickReply(items=[
                            QuickReplyButton(action=LocationAction(label='location'))
                        ]))


class TrashNotFoundResponse(AbstractResponse):
    message_type = 'trash_not_found'
    def create_response(self):
        contents = [
            TextComponent(text=self._context['text'], wrap=True, size='sm'),
        ]
        if self._context['button'] != None:
            contents.append(ButtonComponent(
                style='primary',
                color=Colors['primary'],
                action=PostbackAction(
                    label=self._context['button']['text'],
                    data=self._context['button']['postback']
            )))

        return FlexSendMessage(
            alt_text=self._context['text'],
            contents = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=contents,
                    spacing='md'
                )
            )
        )


class TrashInfoResponse(AbstractResponse):
    message_type = 'trash_info'
    def create_response(self):
        trashinfo = self._context['trash_info'][0]
        contents = [
            TextComponent(
                text=self._context['text'],
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
            alt_text=self._context['text'],
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
                text=self._context['text'],
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
            alt_text=self._context['text'],
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
        return TextSendMessage(text=self._context['text'])


class ResponseAddressRejectResponse(AbstractResponse):
    message_type = 'response_address_reject'
    def create_response(self):
        contents = [
            TextComponent(text=self._context['text'], wrap=True, size='sm'),
        ]
        contents.append(ButtonComponent(
            style='primary',
            color=Colors['primary'],
            action=URIAction(
                label=self._context['button']['text'],
                uri=self._context['button']['uri']
        )))

        return FlexSendMessage(
            alt_text=self._context['text'],
            contents = BubbleContainer(
                body=BoxComponent(
                    layout='vertical',
                    contents=contents,
                    spacing='md'
                )
            )
        )


class HelpSearchTrashResponse(AbstractResponse):
    message_type = 'help_search_trash'
    def create_response(self):
        return TextSendMessage(text=self._context['text'])


ResponseFactory.register_response(
    HelpResponse, ThanksResponse, MistakeResponse,
    RequireAddressResponse, ResponseAddressSuccessResponse, ResponseAddressRejectResponse,
    TrashNotFoundResponse, TrashInfoResponse, TrashSelectResponse,
    HelpSearchTrashResponse)