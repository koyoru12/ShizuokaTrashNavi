import os
import sqlite3
from abc import ABCMeta, abstractclassmethod
from app.db import DatabaseProvider


class CityRepository(metaclass=ABCMeta):
    def __init__(self):
        self._conn = DatabaseProvider.get_connection('trash')
    
    @abstractclassmethod
    def find_city_by_name(self, city_name):
        pass


class CityRDBRepository(CityRepository):
    def find_city_by_name(self, city_name, search_like=False):
        c = self._conn.cursor()
        if search_like:
            c.execute('SELECT * FROM city WHERE city_name LIKE ?', (city_name + '%',))
        else:
            c.execute('SELECT * FROM city WHERE city_name = ?', (city_name,))
        return c.fetchone()

    def find_city_by_id(self, city_id):
        c = self._conn.cursor()
        c.execute('SELECT * FROM city WHERE id = ?', (city_id,))
        return c.fetchone()
