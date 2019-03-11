import env
env.import_environ()
import json

import tornado
from tornado import ioloop, web
from webhooks.router import LineRequestHandler, WebRequestHandler

from app.router import TextMessageRequestHandler, AddressMessageRequestHandler

application = tornado.web.Application([
    (r"/line/webhook", LineRequestHandler),
    (r"/web/webhook", WebRequestHandler),
    (r"/app/message", TextMessageRequestHandler),
    (r"/app/address", AddressMessageRequestHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

