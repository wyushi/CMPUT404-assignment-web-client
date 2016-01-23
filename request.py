import socket
import re
import json
import urllib
from response import HTTPResponse



HTTP_VERSION = 'HTTP/1.1'
CONNECTION_TIMEOUT = socket._GLOBAL_DEFAULT_TIMEOUT;

URL_PATTERN = "^http://(?P<HOST>[A-Za-z0-9\-\.]+)?(:(?P<PORT>[0-9]+))?(?P<PATH>.*)$"


class HTTPRequest(object):

    def __init__(self, url, method='GET', args=None):
        result = re.search(URL_PATTERN, url, re.I)
        # if not result:
        #     print '-----can not parse url: %s----' % url
        self.host = result.group('HOST')
        self.port = result.group('PORT') or '80'
        self.path = result.group('PATH')
        # print '[%s %s %s]' % (self.host, self.port, self.path)
        self.method = method
        if args:
            self.data = urllib.urlencode(args)
        else:
            self.data = None
        self.socket = None

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
        if self.method == 'POST':
            if self.data:
                length = len(self.data)
            else:
                length = 0
            header += self.header_field('Content-Length', length)
            header += self.header_field('Content-Type', 'application/x-www-form-urlencoded')
        else:
            header += self.header_field('Content-Type', 'text/json')
        header += self.header_field('Accept', '*/*')
        header += self.end_header()
        return header

    def request(self):
        req_header = self.header()
        self.send(req_header)
        if self.data != None:
            self.send(self.data)
        return self.socket
        


