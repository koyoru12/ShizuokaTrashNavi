import os
import sqlite3
import json
import re

import tornado
from tornado import gen, httpclient

import util
from app.models import MessageFactory
from app.repositories import (
    FixedReplyRDBRepository, DynamicReplyRDBRepository,
    UserRDBRepository, CityRDBRepository
)


class TextMessageReplyService():
    def __init__(self, request):
        self._request = request
        self._messages = []


    def try_fixed_reply(self):
        repo = FixedReplyRDBRepository()
        data = repo.find_reply_by_message(self._request.request_message)
        if (data):
            # FIX:
            # マッチしたものの最初しか考慮してない
            message = MessageFactory.create_message(data[0]['message_type'], self._request)
            if message is not None:
                self._messages.append(message)
        return self._messages


    def try_dynamic_reply(self):
        q_message = self._request.request_message
        q_city_id = ''

        user_id = self._request.user_id
        user_repo = UserRDBRepository()
        user = user_repo.find_user_by_id(user_id)

        if user is None:
            # ユーザ登録がない場合は静岡市で検索する
            city_repo = CityRDBRepository()
            city = city_repo.find_city_by_name('静岡市')
            q_city_id = city['id']
        else:
            q_city_id = user['city_id']

        reply_repo = DynamicReplyRDBRepository()
        data = reply_repo.find_reply_by_message(q_message, q_city_id)

        message = MessageFactory.create_message('trash_info', self._request)
        message.append_trash_info(data)
        self._messages.append(message)

        if user is None:
            self._messages.append(MessageFactory.create_message('require_address', self._request))
        
        return self._messages


class AddressMessageReplyService():
    def __init__(self, request):
        self._request = request
        self._messages = []

    async def try_register_address(self):
        city_repo = CityRDBRepository()
        city_name = await self._find_address_by_geolocation()
        if city_name == None:
            # 市町村が存在しない場合
            message = MessageFactory.create_message('response_address_reject', self._request)
            self._messages.append(message)
            return self._messages

        city = city_repo.find_city_by_name(city_name)
        if city == None:
            # リクエストされた市町村に対応していない場合
            message = MessageFactory.create_message('response_address_reject', self._request)
            self._messages.append(message)
            return self._messages

        # 市町村情報を登録
        user_repo = UserRDBRepository()
        if user_repo.find_user_by_id(self._request.user_id) == None:
            # ユーザ登録がない場合は登録
            user_repo.register_user(self._request.user_id, city['id'])
        else:
            # ユーザ登録がある場合は更新
            user_repo.update_user(self._request.user_id, city['id'])
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

    