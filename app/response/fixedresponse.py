import os
import sqlite3
import json

import tornado

import util
from app.models.messages import MessageFactory

class FixedResponseHandler():
    @classmethod
    def handle(self, message):
        result = FixedResponseResult()
        sql = 'SELECT * FROM intent WHERE "{message}" LIKE match'.format(message=message)
        c = DbProvider.get_cursor()
        c.execute(sql)
        data = c.fetchone()
        if (data):
            result.resolve = True
            result.message = MessageFactory.create_message(data['message_type'])
        return result
        
class FixedResponseResult(util.JsonSerializable):
    resolve = False
    message = None

class DbProvider():
    dbname = os.path.dirname(__file__) + '/db/fixed_response.db'
    connection = sqlite3.connect(dbname)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    @staticmethod
    def get_cursor():
        return DbProvider.cursor