import os
import sqlite3
from abc import ABCMeta, abstractclassmethod
from app.db import DatabaseProvider


class UserRepository(metaclass=ABCMeta):
    def __init__(self):
        self._conn = DatabaseProvider.get_connection('user')
    
    @abstractclassmethod
    def find_user_by_id(self, city_name):
        pass

    @abstractclassmethod
    def register_user(self, user_id, city_id):
        pass

    @abstractclassmethod
    def update_user(self, user_id, city_id):
        pass


class UserRDBRepository(UserRepository):
    def find_user_by_id(self, user_id):
        c = self._conn.cursor()
        c.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        return c.fetchone()

    def register_user(self, user_id, city_id):
        c = self._conn.cursor()
        c.execute('INSERT INTO user(id, city_id) VALUES(?, ?)', (user_id, city_id))
        self._conn.commit()

    def update_user(self, user_id, city_id):
        c = self._conn.cursor()
        c.execute('UPDATE user SET city_id = ? WHERE id = ?', (city_id, user_id))
        self._conn.commit()

