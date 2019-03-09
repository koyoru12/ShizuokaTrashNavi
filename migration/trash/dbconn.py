import sqlite3

from settings import migrate_settings as SETTINGS


class DatabaseConnection():
    _conn = None
    _connections = {}

    @classmethod
    def get_connection(self, database_path):
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row
        self._connections[database_path] = conn
        return conn
