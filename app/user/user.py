import os
import sqlite3

class Users():
    @classmethod
    def fetch(self, userId):
        c = DbProvider.get_cursor()
        c.execute('SELECT * FROM user WHERE id=:userId', {'userId': userId })
        return c.fetchone()

    @classmethod
    def register(self, userId):
        c = DbProvider.get_cursor()
        c.execute('INSERT INTO user(:userId) VALUES(:userId)', {'userId': userId})

class DbProvider():
    dbname = os.path.dirname(__file__) + '/user.db'
    connection = sqlite3.connect(dbname)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    @staticmethod
    def get_cursor():
        return DbProvider.cursor