#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from request import HTTPRequest 
from response import HTTPResponse 

def help():
    print "httpclient.py [GET/POST] [URL]\n"


class HTTPClient(object):

    def get_host_port(self,url):
        pass

    def get_code(self, header):
        first_line = header.split('\r\n')[0]
        parts = first_line.split(' ')
        return int(parts[1])

    def get_headers(self,data):
        parts = data.split('\r\n\r\n')
        return parts[0]

    def get_body(self, data):
        parts = data.split('\r\n\r\n')
        return parts[1]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def createReponse(self, sock):
        data = self.recvall(sock)
        print 'clent: %s' % data
        header = self.get_headers(data)
        body = self.get_body(data)
        code = self.get_code(header)
        return HTTPResponse(code, body)

    def GET(self, url, args=None):
        req = HTTPRequest(url)
        connection = req.request()
        res = self.createReponse(connection)
        return res

    def POST(self, url, args=None):
        req = HTTPRequest(url, 'POST', args=args)
        connection = req.request()
        res = self.createReponse(connection)
        return res

    def command(self, url, command="GET", args=None):
        # print '<%s, %s, %s>' % (url, command, args)
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    print client.command('http://127.0.0.1:3000/', 'POST', None)
    # if (len(sys.argv) <= 1):
    #     help()
    #     sys.exit(1)
    # elif (len(sys.argv) == 3):
    #     print client.command( sys.argv[1], sys.argv[2] )
    # else:
    #     print client.command( command, sys.argv[1] )    
