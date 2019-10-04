#!/bin/python3
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import os
import re

from tornado.web import RequestHandler
from tornado.escape import utf8


def parsePartHeader(part_header):
    header = part_header.decode('utf-8')
    lines = header.splitlines()

    retData = {}
    for line in lines:
        field, data = line.split(': ', 1)
        retData[field] = data
    return retData


def divideToParts(body, binaryBoundary):
    multiparts = body.split(binaryBoundary)

    parts = []
    for i, part in enumerate(multiparts):
       if len(part) > 0:
           part_header, part_body = part.split(b"\r\n\r\n", 1)

           elem = {}
           elem["header"] = parsePartHeader(part_header)
           elem["body"] = part_body
           parts.append(elem)
    return parts

def parseMultipartForm(body, contentType):
    results = None
    match = re.search(r'boundary=(.*)', contentType)
    if match:
        boundary = match.group(1)

        realBoundary = "--" + boundary + "\r\n"
        binaryBoundary = realBoundary.encode('utf-8')
        results = divideToParts(body, binaryBoundary)
    return results


class BaseHandler(RequestHandler):
    def get(self):
        self.render('dummy.html')

    def post(self):
        headers = self.request.headers
        contentType = headers['Content-Type']
        results = parseMultipartForm(self.request.body, contentType)
        #print(results)
        for i, part in enumerate(results):
            for k, v in part["header"].items():
                print(i, "Header", k, v)
            data = part["body"].decode('utf-8')
            print(i, "data", data)
        
        
        self.render('dummy.html')

        #match = re.search(r'boundary=(.*)', contentType)
        #if match:
        #   boundary = match.group(1)
        #
        #   realBoundary = "--" + boundary + "\r\n"
        #   binaryBoundary = realBoundary.encode('utf-8')
        #   print (binaryBoundary)
        #
        #   data = self.request.body
        #   
        #   multiparts = data.split(binaryBoundary)
        #
        #   print ("*********************************************************************")
        #   print (headers)
        #   
        #   for i, part in enumerate(multiparts):
        #       if len(part) > 0:
        #           print(i)
        #           part_header, part_body = part.split(b"\r\n\r\n", 1)
        #           print (part_header)
        #           print (" ")
        #           print (part_body)
        #
        #   print ("*********************************************************************")
        #   print (data.decode('utf-8'))
        #   self.render('dummy.html')

BASE_DIR = os.path.dirname(__file__)

application = tornado.web.Application(
    [
        (r"/", BaseHandler),
    ],
    template_path=os.path.join(BASE_DIR, 'templates'),
    static_path=os.path.join(BASE_DIR, 'js'),
)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
