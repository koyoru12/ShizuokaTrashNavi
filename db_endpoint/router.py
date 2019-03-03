import tornado
import json
import sqlite3

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
#        print(body)
        sql = 'select 名前, 種類 from sample where 名前 LIKE "%{name}%"'.format(name=body['name'])
        cursor = DbProvider.get_cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        resjson = json.dumps(data, ensure_ascii=False)
        self.write(resjson)
#        self.write('ok')
    def get(self):
        self.write('ok')

class DbProvider():
    dbname = 'db_endpoint/sample.db'
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    @staticmethod
    def get_cursor():
        return DbProvider.cursor