import os
import sqlite3
import json
import re
from abc import ABCMeta, abstractclassmethod

import tornado
from tornado import gen, httpclient

import util
from app.models import MessageFactory
from app.repositories import (
    FixedReplyRDBRepository, DynamicReplyRDBRepository,
    UserRDBRepository, CityRDBRepository
)
from app.services.token import TokenProvider

class TextMessageReplyService():
    def __init__(self, request):
        self._request = request
        self._messages = []
    
    def add_handler(self, handler):
        self._handlers.append(handler)

    def reply(self):
        if self.try_action_reply():
            return self._messages
        if self.try_fixed_reply():
            return self._messages
        if self.try_dynamic_reply():
            return self._messages

    def try_action_reply(self):
        act = self._request.action
        if act.type == '':
            return False
        if act.type == 'help_search_trash':
            # (ヘルプ)ごみの出し方
            message = MessageFactory.create_message('help_search_trash', self._request)
            self._messages.append(message)
            return True
        if act.type == 'help_change_usercity':
            # (ヘルプ)市町村変更
            message = MessageFactory.create_message('help_change_usercity', self._request)
            self._messages.append(message)
            return True
        elif act.type == 'search_trash':
            # 市町村を指定してごみ情報の検索
            # コンフィグ設定を変更する
            self._request.request_message = act.trash
            self._request.config.search_cityid = act.city
            return False
        elif act.type == 'handshake':
            # Web版のハンドシェイク
            message = MessageFactory.create_message('handshake', self._request)
            self._messages.append(message)
            return True
            

        return False

    def try_fixed_reply(self): 
        repo = FixedReplyRDBRepository()
        data = repo.find_reply_by_message(self._request.request_message)
        if (data):
            # FIX:
            # マッチしたものの最初しか考慮してない
            message = MessageFactory.create_message(data[0]['message_type'], self._request)
            if message is not None:
                self._messages.append(message)
                return True
            return False


    def try_dynamic_reply(self):
        user_repo = UserRDBRepository()
        city_repo = CityRDBRepository()

        def check_city_assginment():
            # 検索語に市町村が指定されているか確認する
            m = re.match('(.+)[\s|　]+(.+)', self._request.request_message)
            if m:
                city_name = m.group(1)
                trash_name = m.group(2)
                city_data = city_repo.find_city_by_name(city_name, search_like=True)
                if city_data != None:
                    # 市町村指定があるときはリクエストを書き換える
                    # ex)静岡　ペットボトル
                    self._request.request_message = trash_name
                    city = city_repo.find_city_by_name(city_data['city_name'])
                    if city != None:
                        self._request.config.search_cityid = city['id']

        check_city_assginment()

        q_message = self._request.request_message
        q_city_id = ''
        user_id = self._request.user_id
        user = user_repo.find_user_by_id(user_id)
        if self._request.config.search_cityid != '':
            # 市町村IDが指定されている場合は優先
            q_city_id = self._request.config.search_cityid
        else:
            if user == None:
                # ユーザ登録がない場合は静岡市で検索する
                city = city_repo.find_city_by_name('静岡市')
                q_city_id = city['id']
            else:
                # ユーザ登録がある場合は登録された市町村で検索する
                q_city_id = user['city_id']

        reply_repo = DynamicReplyRDBRepository(q_message, q_city_id)
        trash_list = reply_repo.find_reply_by_message()

        if len(trash_list) == 0:
            # 結果が見つからない場合
            if q_city_id == '*':
                # すべての市町村で見つからなかった場合
                message = MessageFactory.create_message('trash_not_found', self._request)
                self._messages.append(message)
            else:
                # 特定の市町村で検索した場合は「他の市町村で探す」ボタンを表示
                message = MessageFactory.create_message('trash_not_found', self._request, searchbutton=True)
                self._messages.append(message)

        elif 0 < len(trash_list) <= 3:
            # 結果が3個以下の場合はすべてメッセージにする
            for trash in trash_list:
                message = MessageFactory.create_message('trash_info', self._request, trash=trash)
                self._messages.append(message)        
        else:
            # 結果が4個以上の場合は選択肢にする
            # 上限10個
            trash_list = trash_list[0:10]
            message = MessageFactory.create_message('trash_select', self._request,
                trash_list=trash_list, show_city=True)
            self._messages.append(message)

        if user is None and self._request.client == 'line':
            # LINEでユーザ登録がない場合は登録を促す
            # 暫定的に機能停止中
            # self._messages.append(MessageFactory.create_message('require_address', self._request))
            pass
        
        return True


class AddressMessageReplyService():
    def __init__(self, request):
        self._request = request
        self._messages = []

    async def try_register_address(self):
        city_repo = CityRDBRepository()
        city_name = await self._find_address_by_geolocation()
        if city_name == None:
            # 市町村が存在しない場合はWebサイトに誘導
            token = TokenProvider.issue(self._request.user_id)
            message = MessageFactory.create_message('response_address_reject', self._request, token=token)
            self._messages.append(message)
            return self._messages

        city = city_repo.find_city_by_name(city_name)
        if city == None:
            # リクエストされた市町村に対応していない場合はWebサイトに誘導
            token = TokenProvider.issue(self._request.user_id)
            message = MessageFactory.create_message('response_address_reject', self._request, token=token)
            self._messages.append(message)
            return self._messages

        # 市町村情報を登録
        CityService.register_user_city(self._request.user_id, city['id'])
        message = MessageFactory.create_message('response_address_success', self._request, city_name=city_name)
        self._messages.append(message)
        return self._messages

    async def _find_address_by_geolocation(self):
        def strip_ward_from_city_name(city_name):
            m = re.match('(.+市).+区', city_name)
            return None if m == None else m.group(1)

        url = 'http://geoapi.heartrails.com/api/json?method=searchByGeoLocation&x={}&y={}'.format(
            self._request.longitude,
            self._request.latitude
        )
        # FIX:
        # http失敗時のエラーハンドリング
        http_client = httpclient.AsyncHTTPClient()
        raw_response = await http_client.fetch(url)
        raw_body = raw_response.body.decode('utf-8')
        response = json.loads(raw_body)

        if 'location' in response['response']:
            city_name = response['response']['location'][0]['city']
            stripped = strip_ward_from_city_name(city_name)
            return city_name if stripped == None else stripped                
        else:
            return None


class CityService:
    @classmethod
    def get_all_city(self):
        repo = CityRDBRepository()
        return repo.get_all_city()

    @classmethod
    def register_user_city(self, user_id, city_id):
        user_repo = UserRDBRepository()
        if user_repo.find_user_by_id(user_id) == None:
            # ユーザ登録がない場合は登録
            user_repo.register_user(user_id, city_id)
        else:
            # ユーザ登録がある場合は更新
            user_repo.update_user(user_id, city_id)
