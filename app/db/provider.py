import os
import sqlite3

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

