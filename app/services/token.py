import os
import datetime

import jwt


class TokenProvider:
    secret_key = os.environ['TOKEN_SECRET']
    
    @classmethod
    def issue(self, user_id):
        """認証トークンを発行する
        """
        encoded = jwt.encode({
            'user_id': user_id,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, self.secret_key).decode()
        return encoded

    @classmethod
    def authenticate(self, token):
        try:
            decoded = jwt.decode(token, self.secret_key)
            return decoded['user_id']
        except Exception as e:
            print(e)
            return False