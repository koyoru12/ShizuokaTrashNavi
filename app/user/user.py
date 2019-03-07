import os
import sqlite3

from app.db import DatabaseProvider


class Users():
    @classmethod
    def fetch(self, user_id):
        c = DatabaseProvider.get_connection('user').cursor()
        c.execute('SELECT * FROM user WHERE id=?', (user_id,))
        return c.fetchone()

    @classmethod
    def register(self, user_id, city_id):
        c = DatabaseProvider.get_connection('user').cursor()
        c.execute('INSERT INTO user(?) VALUES(?)', (user_id, city_id))


