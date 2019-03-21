import datetime
import os

from app.db import DatabaseProvider

class ChatLogger():
    @classmethod
    def initialize(self):
        conn = self._get_conn()
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS chatlog(
            timestamp NOT NULL,
            user_id TEXT,
            client TEXT,
            request TEXT,
            response TEXT
        )
        """)

    @classmethod
    def log(self, request, response):
        for message in response.messages:
            if os.environ['env'] == 'dev':
                print(message.to_json())
            else:
                self._insert(request, message)

    @classmethod
    def _insert(self, request, message):
        conn = self._get_conn()
        c = conn.cursor()
        sql = """
        INSERT INTO chatlog VALUES(
            :timestamp,
            :user_id,
            :client,
            :request,
            :response
        )
        """
        c.execute(sql, {
            'timestamp': datetime.datetime.utcnow(),
            'user_id': request.user_id,
            'client': request.client,
            'request': request.request_message,
            'response': message.type
        })
        conn.commit()

    @classmethod
    def _get_conn(self):
        return DatabaseProvider.get_connection('chatlog')


ChatLogger.initialize()