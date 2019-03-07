import os
import sqlite3


class City():
    @classmethod
    def fetch(self, city_name):
        c = DatabaseProvider.get_connection('trash').cursor()
        c.execute('SELECT * FROM city WHERE city_name = ?', (city_name,))
        return c.fetchone()


class User():
    @classmethod
    def fetch(self, user_id):
        c = DatabaseProvider.get_connection('user').cursor()
        c.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        return c.fetchone()

    @classmethod
    def register(self, user_id, city_id):
        c = DatabaseProvider.get_connection('user').cursor()
        c.execute('INSERT INTO user(id, city_id) VALUES(?, ?)', (user_id, city_id))

    @classmethod
    def update(self, user_id, city_id):
        c = DatabaseProvider.get_connection('user').cursor()
        c.execute('UPDATE user SET city_id = ? WHERE id = ?', (city_id, user_id))


class DatabaseProvider():
    _connections = {}
    @classmethod
    def append_connection(self, name, uri):
        self._connections[name] = sqlite3.connect(uri)
        self._connections[name].row_factory = sqlite3.Row

    @classmethod
    def get_connection(self, name):
        if name in self._connections:
            return self._connections[name]
        raise Exception('Name not found > ' + name)

dbdir = str(os.environ.get('DATABASE_DIR'))
DatabaseProvider.append_connection('user', dbdir + '/user.db')
DatabaseProvider.append_connection('trash', dbdir + '/trash.db')

