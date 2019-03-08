import os
import sqlite3
from abc import ABCMeta, abstractclassmethod
from app.db import DatabaseProvider

class UserRepository(metaclass=ABCMeta):
    def __init__(self):
        self._conn = DatabaseProvider.get_connection('user')
    
    @abstractclassmethod
    def find_city_by_name(self, city_name):
        pass


class UserRDBRepository(UserRepository):
    def find_city_by_name(self, city_name):
        c = self._conn.cursor()
        c.execute('SELECT * FROM city WHERE city_name = ?', (city_name,))
        return c.fetchone()


class FixedReplyRepository(metaclass=ABCMeta):
    def __init__(self):
        self._conn = DatabaseProvider.get_connection('trash')

    @abstractclassmethod
    def find_reply_by_message(self, request_message):
        pass


class FixedReplyRDBRepository(FixedReplyRepository):
    def find_reply_by_message(self, request_message):
        c = self._conn.cursor()
        c.execute('SELECT * FROM fixedreply WHERE ? LIKE match',
                  (request_message,))
        return c.fetchall()


class DynamicReplyRepository(metaclass=ABCMeta):
    def __init__(self):
        self._conn = DatabaseProvider.get_connection('trash')

    @abstractclassmethod
    def find_reply_by_message(self, request_message, city_id):
        pass


class DynamicReplyRDBRepository(DynamicReplyRepository):
    def find_reply_by_message(self, request_message, city_id):
        c = self._conn.cursor()
        c.execute("""
        SELECT trash.name, trash.category, trash.note, city.city_name
            FROM trash, city
            WHERE trash.city_id = city.id
            AND trash.name LIKE ?
            AND trash.city_id = ?
        """, ('%' + request_message + '%', city_id))
        return c.fetchone()

