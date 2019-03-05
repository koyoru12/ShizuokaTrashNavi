import os
import tornado
import json
import sqlite3

class TrashDbHandler():
    @classmethod
    def handle(self, message):
        sql = 'select 名前, 種類 from sample where 名前 LIKE "%{name}%"'.format(name=message)
        cursor = DbProvider.get_cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        return data

class DbProvider():
    dbname = os.path.dirname(__file__) + '/db/sample.db'
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    @staticmethod
    def get_cursor():
        return DbProvider.cursor