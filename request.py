import socket
import re
import json
import urllib
from response import HTTPResponse



HTTP_VERSION = 'HTTP/1.1'
CONNECTION_TIMEOUT = socket._GLOBAL_DEFAULT_TIMEOUT;

URL_PATTERN = "^http://(?P<HOST>[A-Za-z0-9\-\.]+)?(:(?P<PORT>[0-9]+))?(?P<PATH>.*)$"


def nice_print(title, header):
        print '-' * 10 + ' ' + title + ' ' + '-' * 10
        print header + '-' * 28

class HTTPRequest(object):

    def __init__(self, url, method='GET', args=None):
        self.socket = None

        result = re.search(URL_PATTERN, url, re.I)
        self.host = result.group('HOST')
        self.port = result.group('PORT') or '80'
        self.path = result.group('PATH')
        self.method = method

        if args:
            self.data = encode_data(args)
        else:
            self.data = None
        

    def encode_data(self, data):
        return urllib.urlencode(data)


    def connect(self):
        self.socket = socket.create_connection((self.host, self.port), CONNECTION_TIMEOUT)


    def send(self, content):
        if self.socket == None:
            self.connect()
        self.socket.sendall(content)


    def start_header(self):
        return "%s %s %s\r\n" % (self.method, self.path, HTTP_VERSION)


    def header_field(self, field, value):
        return "%s: %s\r\n" % (field, value)


    def end_header(self):
        return "\r\n"


    def header(self):
        header = self.start_header()
        header += self.header_field('Host', self.host)
        header += self.header_field('Accept', '*/*')

        if self.method == 'GET':
            self.GET_header(header)
        elif self.method == 'POST':
            self.POST_header(header)
        
        header += self.header_field('Connection', 'close')
        header += self.end_header()
        return header


    def GET_header(self, header):
        pass


    def POST_header(self, header):
        length = len(self.data or '')
        header += self.header_field('Content-Length', length)
        header += self.header_field('Content-Type', 'application/x-www-form-urlencoded')


    def request(self):
        req_header = self.header()
        self.send(req_header)
        nice_print('header', req_header)
        if self.data != None:
            self.send(self.data)
        return self.socket


    
        


