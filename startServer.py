#!/usr/bin/python3
"""
ssh cvteam1@134.173.43.20
cd compData
python startServer.py
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import curdir
import json
from copy import deepcopy


class requestHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        SimpleHTTPRequestHandler.do_GET(self)

    def do_PUT(self):
        # refuse to receive non-json content
        if self.headers['content-type'] != 'application/json':
            self.send_response(400, 'content-type is not json')
            self.end_headers()
            return

        # check that url is correct:
        if not self.path.endswith('.txt'):
            self.send_response(400, 'Bad url')
            self.end_headers()
            return

        uploadpath = curdir + self.path
        # print('self headers\n', self.headers)

        # read the message and convert it into a python dictionary
        length = self.headers['content-length']
        databyt = self.rfile.read(int(length))
        datajson = json.loads(databyt)

        with open(uploadpath, 'w') as fh:
            # write the bbox data to the text file on the server
            if 'bboxes' in datajson:
                fh.write(datajson['bboxes'])
            elif 'numLabeled' in datajson:
                fh.write(datajson['numLabeled'])

        self.send_response(201, 'Created')

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
