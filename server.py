import tornado.ioloop
import tornado.web
import importenv
from line_endpoint.router import LineApiHandler
from db_endpoint.router import MainHandler

application = tornado.web.Application([
    (r"/line/webhook", LineApiHandler),
    (r"/gateway", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

