import os
import sqlite3
import json

import tornado

import util
from app.models import MessageFactory
from app.db import DatabaseProvider

class FixedReplyHandler():
    @classmethod
    def handle(self, request_body):
        c = DatabaseProvider.get_connection('trash').cursor()
        c.execute('SELECT * FROM fixedreply WHERE ? LIKE match',
                  (request_body.request_message,))
        data = c.fetchone()
        message = None
        if (data):
            message = MessageFactory.create_message(data['message_type'], request_body)
        return message
        

