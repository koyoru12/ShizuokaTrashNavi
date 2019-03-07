import os
import sqlite3
import json

import tornado

import util
from app.models import MessageFactory
from app.db import DatabaseProvider

class FixedReplyHandler():
    def __init__(self, request):
        self._request = request
        self._messages = []

    def handle(self):
        c = DatabaseProvider.get_connection('trash').cursor()
        c.execute('SELECT * FROM fixedreply WHERE ? LIKE match',
                  (self._request.request_message,))
        data = c.fetchone()
        if (data):
            message = MessageFactory.create_message(data['message_type'], self._request)
            if message is not None:
                self._messages.append(message)
        return self._messages
        

