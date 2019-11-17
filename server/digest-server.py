#!/bin/python3
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import os

from tornado.web import RequestHandler
from tornado.escape import utf8
from hashlib import md5

class BaseHandler(RequestHandler):
    def get(self):
        self.render('index.html')
 
class BasicAuthHandler(RequestHandler):
    def get(self):
        realm = 'renjie'
        username = 'foo'
        password = 'bar'
        # Authorization: Basic base64("user:passwd")
        auth_header = self.request.headers.get('Authorization', None)
        if auth_header is not None:
            # Basic Zm9vOmJhcg==
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            assert auth_mode == 'Basic'
            # 'Zm9vOmJhcg==' == base64("foo:bar")
            auth_username, auth_password = auth_base64.decode('base64').split(':', 1)
            if auth_username == username or auth_password == password:
                self.write('ok')
            else:
                self.write('fail')
        else:
            '''
            HTTP/1.1 401 Unauthorized
            WWW-Authenticate: Basic realm="renjie"
            '''
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="%s"' % realm)
 
class DigestAuthHandler(RequestHandler):
    def post(self):
        realm = 'test'
        opaque = 'asdf'
        # Real implementations would use a random nonce.
        nonce = "1234"
        username = 'foo'
        password = 'bar'
        '''
        Authorization: Digest username="foo", 
                              realm="test", 
                              nonce="1234", 
                              uri="/auth/digest", 
                              response="e839337ef079c93238a4bf4f1ae712b3", 
                              opaque="asdf"
        '''
        auth_header = self.request.headers.get('Authorization', None)
        if auth_header is not None:
            auth_mode, params = auth_header.split(' ', 1)
            assert auth_mode == 'Digest'
            param_dict = {}
            for pair in params.split(','):
                k, v = pair.strip().split('=', 1)
                if v[0] == '"' and v[-1] == '"':
                    v = v[1:-1]
                param_dict[k] = v
            assert param_dict['realm'] == realm
            assert param_dict['opaque'] == opaque
            assert param_dict['nonce'] == nonce
            assert param_dict['username'] == username
            assert param_dict['uri'] == self.request.path
            h1 = md5(utf8('%s:%s:%s' % (username, realm, password))).hexdigest()
            h2 = md5(utf8('%s:%s' % (self.request.method,
                                     self.request.path))).hexdigest()
            digest = md5(utf8('%s:%s:%s' % (h1, nonce, h2))).hexdigest()
            if digest == param_dict['response']:
                self.write('ok')
            else:
                self.write('fail')
        else:
            self.set_status(401)
            # WWW-Authenticate: Digest realm="test", nonce="1234", opaque="asdf"
            self.set_header('WWW-Authenticate',
                            'Digest realm="%s", nonce="%s", opaque="%s"' %
                            (realm, nonce, opaque))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

BASE_DIR = os.path.dirname(__file__)

application = tornado.web.Application(
    [
        (r"/", BaseHandler),
        (r"/login/", DigestAuthHandler)
    ],
    template_path=os.path.join(BASE_DIR, 'templates'),
    static_path=os.path.join(BASE_DIR, 'js'),
)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
