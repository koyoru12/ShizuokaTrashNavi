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


class HelpMessage(AbstractMessage):
    message_type = 'help'
    def __init__(self, context):
        super().__init__(context)
        self.body = {
            'head': 'こんにちは！わたしにできることはありますか？',
            'contents': [
                {
                    'text': 'ごみの分別の仕方を調べたい！',
                    'postback': 'action?type=help_search_trash'
                },
                {
                    'text': '検索する市町村を変えたい！',
                    'postback': 'action?type=help_change_address'
                }
            ]
        }


class ThanksMessage(AbstractMessage):
    message_type = 'thanks'
    def __init__(self, context):
        super().__init__(context)
        self.body = 'どういたしまして！\nお役に立てて嬉しいです😊'


class MistakeMessage(AbstractMessage):
    message_type = 'mistake'
    def __init__(self, context):
        super().__init__(context)
        self.body = 'ごめんなさい。\nお役に立てなくて残念です😔'


class RequireAddressMessage(AbstractMessage):
    message_type = 'require_address'
    def __init__(self, context):
        super().__init__(context)
        self.body = {
            'line': 'まだ地域を登録していないみたいですね。\n'
                    + '下のボタンをタップしてお住まいの地域を教えてください！✨\n'
                    + 'お住まいの地域の情報を検索できるかも知れませんよ😉'
        }


class ResponseAddressSuccessMessage(AbstractMessage):
    message_type = 'response_address_success'
    def __init__(self, context, city_name):
        super().__init__(context)
        # FIX:
        # 地域変更の案内
        self.body = ('地域を登録しました！✨\n次から{}でごみ分別情報を検索しますね😉\n'
            '地域を変更するには位置情報を送るか、「ヘルプ」と言ってみてください！'
            ).format(city_name)


class ResponseAddressRejectMessage(AbstractMessage):
    message_type = 'response_address_reject'
    def __init__(self, context):
        super().__init__(context)
        # FIX:
        # 登録できる市町村の案内
        self.body = 'ごめんなさい〜！😣\nその市町村には対応していないんです…。'


class TrashInfoMessage(AbstractMessage):
    message_type = 'trash_info'
    def __init__(self, context, trash=None):
        super().__init__(context)
        self.body = ''
        self.trash_info = []

        if trash == None:
            self.body = 'ごめんなさい〜！😣\n情報が見つかりませんでした…。'
        else:
            trash_dict = {}
            self.body = trash['city_name'] + 'でこんな情報が見つかりました！'
            for key in trash.keys():
                trash_dict[key] = trash[key]
            self.trash_info.append(trash_dict)


class TrashSelectMessage(AbstractMessage):
    message_type = 'trash_select'
    def __init__(self, context, trash_list=None):
        super().__init__(context)
        self.body = 'いくつか候補が見つかりました！下の選択肢から選んでください✨'
        self.trash_list = []

        for trash in trash_list:
            self.trash_list.append(trash['name'])

MessageFactory.register_message(
    HelpMessage, ThanksMessage, MistakeMessage,
    RequireAddressMessage, ResponseAddressSuccessMessage,
    ResponseAddressRejectMessage, TrashInfoMessage, TrashSelectMessage)