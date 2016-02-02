import socket
import re
import json
from urllib import urlencode
from response import HTTPResponse



HTTP_VERSION = 'HTTP/1.1'
CONNECTION_TIMEOUT = socket._GLOBAL_DEFAULT_TIMEOUT;

URL_PATTERN = "^(http://)?(?P<HOST>[A-Za-z0-9\-\.]+)?(:(?P<PORT>[0-9]+))?(?P<PATH>[^\\?]*)(?P<QURY>(.*))$"


def nice_print(title, header):
        print '-' * 10 + ' ' + title + ' ' + '-' * 10
        print header + '-' * 28

class HTTPRequest(object):

    
    def __init__(self, url, method='GET', args=None):
        self.socket = None
        self.method = method
        self.parse_url(url)
        self.data = None

        if self.method == 'GET':
            self.path += (self.query_params(args) or '')
        elif self.method == 'POST':
            self.path += self.query
            self.data = urlencode(args or '')
            

    def query_params(self, args):
        if args is None:
            return self.query
        
        if not self.query.strip():
            self.query = '?'
        else:
            self.query += '&'

        return self.query + urlencode(args)


    def parse_url(self, url):
        if not url.startswith('http://'):
            url = 'http://' + url
        result = re.search(URL_PATTERN, url, re.I)
        self.host = result.group('HOST')
        self.port = result.group('PORT') or '80'
        self.path = result.group('PATH')
        self.query = result.group('QURY')


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

        if self.method == 'POST':
            length = len(self.data or '')
            header += self.header_field('Content-Length', length)
            header += self.header_field('Content-Type', 'application/x-www-form-urlencoded')
        
        header += self.header_field('Connection', 'close')
        header += self.end_header()
        return header


    def GET_header(self, header):
        return header


    def POST_header(self, header):
        
        return header


    def request(self):
        req_header = self.header()
        # nice_print('header', req_header)
        self.send(req_header)
        if self.data != None:
            self.send(self.data)
        return self.socket


    
        


