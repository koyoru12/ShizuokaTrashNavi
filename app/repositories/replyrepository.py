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
    def __init__(self, request_message, city_id):
        self._conn = DatabaseProvider.get_connection('trash')
        self._req = request_message
        self._city_id = city_id

    @abstractclassmethod
    def find_reply_by_message(self):
        pass


class DynamicReplyRDBRepository(DynamicReplyRepository):
    def find_reply_by_message(self):
        self._handlers = []
        def add_handler(func):
            self._handlers.append(func)
        
        def handle():
            for handler in self._handlers:
                rows = handler()
                if len(rows) > 0:
                    return rows
            return []

        add_handler(self._find_from_trash)
        add_handler(self._find_like_from_trash)
        add_handler(self._find_from_synonym)
        return handle()

    def _find_from_trash(self):
        c = self._conn.cursor()
        if self._city_id == '':
            sql = """
            SELECT trash.*, city.city_name
                FROM trash, city
                WHERE trash.city_id = city.id
                AND trash.name = ?
            """
            c.execute(sql, (self._req,))
        else:
            sql = """
            SELECT trash.*, city.city_name
                FROM trash, city
                WHERE trash.city_id = city.id
                AND trash.name = ?
                AND trash.city_id = ?
            """
            c.execute(sql, (self._req, self._city_id))
        return c.fetchall()

    def _find_like_from_trash(self):
        c = self._conn.cursor()
        sql = """
        SELECT trash.*, city.city_name
            FROM trash, city
            WHERE trash.city_id = city.id
            AND trash.city_id = ?
            AND (trash.name LIKE ? OR ? LIKE '%'||trash.name||'%')
        """
        c.execute(sql, (self._city_id, '%' + self._req + '%', self._req))
        return c.fetchall()

    def _find_from_synonym(self):
        c = self._conn.cursor()
        sql = """
        SELECT trash.*, city.city_name
            FROM trash, trash_synonym, synonym, city
            WHERE trash.city_id = city.id
            AND trash.city_id = ?
            AND trash.id = trash_synonym.trash_id
            AND synonym.id = trash_synonym.synonym_id
            AND (synonym.name LIKE ? OR ? LIKE '%'||synonym.name||'%') 
        """
        c.execute(sql, (self._city_id, '%' + self._req + '%', self._req))
        return c.fetchall()

        