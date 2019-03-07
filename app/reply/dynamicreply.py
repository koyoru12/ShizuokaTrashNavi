import os
import tornado
import json
import sqlite3

from app.models import MessageFactory
from app.db import DatabaseProvider, User


class DynamicReplyHandler():
    def __init__(self, request):
        self._request = request
        self._messages = []
        user_id = self._request.user_id
        self._user = User.fetch(user_id)


    def handle(self):
        cursor = DatabaseProvider.get_connection('trash').cursor()

        q_name = '%' + self._request.request_message + '%'
        q_city_id = ''
        if self._user is None:
            cursor.execute("""
            SELECT id FROM city
                WHERE city_name = "静岡市"
            """)
            q_city_id = cursor.fetchone()['id']
        else:
            q_city_id = self._user['city_id']

        cursor.execute("""
        SELECT trash.name, trash.category, trash.note, city.city_name
            FROM trash, city
            WHERE trash.city_id = city.id
            AND trash.name LIKE ?
            AND trash.city_id = ?
        """, (q_name, q_city_id))
        data = cursor.fetchone()

        message = MessageFactory.create_message('trash_info', self._request)
        message.append_trash_info(data)
        self._messages.append(message)

        if self._user is None:
            self._messages.append(MessageFactory.create_message('require_address', self._request))
        
        return self._messages

