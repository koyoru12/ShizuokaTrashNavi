import os
import tornado
import json
import sqlite3

from app.models import MessageFactory
from app.db import DatabaseProvider


class DynamicReplyHandler():
    @classmethod
    def handle(self, request_body):
        c = DatabaseProvider.get_connection('trash').cursor()
        c.execute("""
        SELECT name, category FROM trash
            WHERE name LIKE ?
        """, ('%' + request_body.request_message + '%',))
        data = c.fetchone()
        message = MessageFactory.create_message('trash_info', request_body)
        message.append_trash_info(data)
        return message


