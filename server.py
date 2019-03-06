import env
env.import_environ()
import json
import tornado
from tornado import ioloop, web
from line.router import LineWebRequestHandler
from app.router import TextMessageRequestHandler, AddressMessageRequestHandler

application = tornado.web.Application([
    (r"/line/webhook", LineWebRequestHandler),
    (r"/app/message", TextMessageRequestHandler),
    (r"/app/address", AddressMessageRequestHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

