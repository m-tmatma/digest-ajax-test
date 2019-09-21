import tornado.ioloop
import tornado.web
import os
import logging

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

def log_function(reqHandler):
    req = reqHandler.request
    for k, v in req.__dict__.items():
        print (k, ":", v)

if __name__ == "__main__":
    app = make_app()
    app.settings["log_function"] = log_function

    server = tornado.httpserver.HTTPServer(app, idle_connection_timeout=10.0)
    server.bind(80)
    server.start()
#   app.listen(80)
    tornado.ioloop.IOLoop.current().start()
