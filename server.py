import env
env.import_environ()

import json
import os

import tornado
from tornado import ioloop, web, httpserver
from webhooks.router import LineRequestHandler, WebRequestHandler

from app.router import (TextMessageRequestHandler, AddressMessageRequestHandler, GetValidCityHandler,
                       LineTokenAuthenticationHandler, ChangeUserCityHandler, ContactHandler)

application = tornado.web.Application([
    (r"/api/line/webhook", LineRequestHandler),
    (r"/api/web/webhook", WebRequestHandler),
    (r"/api/app/message", TextMessageRequestHandler),
    (r"/api/app/address", AddressMessageRequestHandler),
    (r"/api/app/city", GetValidCityHandler),
    (r"/api/app/authentication", LineTokenAuthenticationHandler),
    (r"/api/app/usercity", ChangeUserCityHandler),
    (r"/api/app/contact", ContactHandler)
])

if __name__ == "__main__":
    server = httpserver.HTTPServer(application, ssl_options={
        'certfile': '/etc/letsencrypt/live/www.smallnight.net/fullchain.pem',
        'keyfile': '/etc/letsencrypt/live/www.smallnight.net/privkey.pem'
    })
    if os.environ['env'] == 'dev':
        application.listen(8888)
    else:
        server.listen(8888)
    tornado.ioloop.IOLoop.current().start()

