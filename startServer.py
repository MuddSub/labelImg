#!/usr/bin/python3
"""
ssh cvteam1@134.173.43.20
cd compData
python startServer.py
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import curdir
import json


class requestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        SimpleHTTPRequestHandler.do_GET(self)

    def do_PUT(self):
        if self.path.endswith('.txt'):
            uploadpath = curdir + self.path
            # print('self headers\n', self.headers)
            length = self.headers['content-length']
            databyt = self.rfile.read(int(length))
            # print(type(databyt))
            # print(databyt)
            datajson = json.loads(databyt)
            # print('datajson\n', datajson)

            with open(uploadpath, 'w') as fh:
                fh.write(datajson['bboxes'])

            self.send_response(200)
            # self.send_response(201, 'Created')
            # self.send_header("Content-type", "text/html")

            self.end_headers()

    def do_POST(self):
        self.do_PUT()


def main():
    PORT = 8080
    httpd = HTTPServer(('', PORT), requestHandler)  #http daemon
    print('server running on port %s' % PORT)
    httpd.serve_forever()


if __name__ == '__main__':
    # i.e. if this file is being run directly, not as imported module
    main()
