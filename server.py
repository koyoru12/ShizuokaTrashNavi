import env
env.import_environ()
import json
import tornado
from tornado import ioloop, web
from line_endpoint.router import LineWebRequestHandler
from app_gateway.router import AppGatewayHandler

application = tornado.web.Application([
    (r"/line/webhook", LineWebRequestHandler),
    (r"/app/gateway", AppGatewayHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

