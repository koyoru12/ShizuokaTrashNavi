import os

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
    message_type = ''
    def __init__(self, context):
        self._context = context
        self.type = self.message_type


class HandShakeMessage(AbstractMessage):
    message_type = 'handshake'
    def __init__(self, context, trash_list=None):
        super().__init__(context)
        self.text = 'こんにちは！\n捨てたいごみの名前を教えてください！\n使い方を知りたいときは「ヘルプ」と呟いてみてくださいね😉'


class HelpMessage(AbstractMessage):
    message_type = 'help'
    def __init__(self, context):
        super().__init__(context)
        self.text = 'こんにちは！わたしにできることはありますか？'
        self.contents = [
                {
                    'text': 'ごみの分別の仕方を調べたい！',
                    'postback': 'type=help_search_trash'
                },
                {
                    'text': '検索する市町村を変えたい！',
                    'postback': 'type=help_change_usercity'
                }
        ]


class ThanksMessage(AbstractMessage):
    message_type = 'thanks'
    def __init__(self, context):
        super().__init__(context)
        self.text = 'どういたしまして！\nお役に立てて嬉しいです😊'


class MistakeMessage(AbstractMessage):
    message_type = 'mistake'
    def __init__(self, context):
        super().__init__(context)
        self.text = 'ごめんなさい。\nお役に立てなくて残念です😔'


class RequireAddressMessage(AbstractMessage):
    message_type = 'require_address'
    def __init__(self, context):
        super().__init__(context)
        self.text = ('まだ地域を登録していないみたいですね。\n'
                     '下のボタンをタップしてお住まいの地域を教えてください！✨\n'
                     'お住まいの地域の情報を検索できるかも知れませんよ😉')


class ResponseAddressSuccessMessage(AbstractMessage):
    message_type = 'response_address_success'
    def __init__(self, context, city_name):
        super().__init__(context)
        self.text = ('地域を登録しました！✨\n次から{}でごみ分別情報を検索しますね😉\n'
            '地域を変更するには位置情報を送るか、「ヘルプ」と言ってみてください！'
            ).format(city_name)


class ResponseAddressRejectMessage(AbstractMessage):
    message_type = 'response_address_reject'
    def __init__(self, context, token=''):
        super().__init__(context)
        self.text = ('ごめんなさい〜！😣\nその市町村には対応していないんです…。\n'
                     '対応している市町村は次のページのとおりです。')
        self.button = {
            'text': '市町村を変更する',
            'uri': '{}?token={}'.format( os.environ['URI_SELECTCITY'], token)
        }

class TrashNotFoundMessage(AbstractMessage):
    message_type = 'trash_not_found'
    def __init__(self, context, searchbutton=False):
        super().__init__(context)
        if searchbutton:
            self.text = 'ごめんなさい〜！😣\n情報が見つかりませんでした…。'
            self.button = {
                'text': '他の市町村で探してみる',
                'postback': 'type=search_trash&trash={}&city=*'.format(self._context.request_message)
            }
        else:
            self.text = 'ごめんなさい〜！😣\n情報が見つかりませんでした…。\n他の言葉に言い換えて試してみてください！'
            self.button = None

class TrashInfoMessage(AbstractMessage):
    message_type = 'trash_info'
    def __init__(self, context, trash):
        super().__init__(context)
        self.text = ''
        self.trash_info = []

        trash_dict = {}
        self.text = trash['city_name'] + 'でこんな情報が見つかりました！'
        for key in trash.keys():
            trash_dict[key] = trash[key]
        self.trash_info.append(trash_dict)


class TrashSelectMessage(AbstractMessage):
    message_type = 'trash_select'
    def __init__(self, context, trash_list=None, show_city=False):
        super().__init__(context)
        self.text = 'いくつか候補が見つかりました！下の選択肢から選んでください✨'
        self.trash_list = []

        for trash in trash_list:
            sub = ''
            if show_city:
                sub = trash['city_name'] + '　'
            sub += trash['name']
            self.trash_list.append(sub)
    

class HelpSearchTrashMessage(AbstractMessage):
    message_type = 'help_search_trash'
    def __init__(self, context, trash_list=None):
        super().__init__(context)
        self.text = ('どんなごみか教えてください！\n'
                     'たとえばペットボトルなら「ペットボトル」と言うだけで大丈夫ですよ😉')
        
    
class HelpChangeUserCityMessage(AbstractMessage):
    message_type = 'help_change_usercity'
    def __init__(self, context, trash_list=None):
        super().__init__(context)
        if context.client == 'line':
            self.text = '分かりました！\n下のボタンをタップして位置情報を送ってください😉'
        else:
            self.text = '分かりました！\nメッセージ欄の左側にある設定ボタンをクリックしてみてください😉'


MessageFactory.register_message(
    HandShakeMessage, HelpMessage, ThanksMessage, MistakeMessage,
    RequireAddressMessage, ResponseAddressSuccessMessage, ResponseAddressRejectMessage,
    TrashNotFoundMessage, TrashInfoMessage, TrashSelectMessage,
    HelpSearchTrashMessage, HelpChangeUserCityMessage
    )