#!/usr/bin/python
#coding=utf-8

import socket
import httplib,urlparse, cookielib, urllib, urllib2
from PackageHTTP.UserAgents import getRandomAgent
'''
    response.geturl()
    返回302重定向后的页面url
'''
'''
    response.info()
    返回http response头
'''


'''
    openers/handlers

    创建一个自定义的opener,通过给opener绑定handler

    opener的创建:
        OpenerDirector
        build_opener

    (全局默认opener由install_opener创建)
'''
class Method:
    def __init__(self):
        self.request = None
        self.opener = urllib2.build_opener()
        self.hostname = None
        self.port = None
        self.url = None

    def setHostInfo(self,hostname = None,port = 80,url=None):
        if url != None:
            self.url = url
        else:
            self.hostname = hostname
            self.port = port
            self.url = 'http://%s:%d' %(self.hostname, self.port)
        '''
        if len(url) != 0:
            u = urlparse.urlparse(url)
            u = u.netloc.split(':')
            self.host = u[0]
            if len(u) == 2:
                self.port = u[1]
        '''

    '''
    HTTPHeader中的Cookie可直接拷贝使用
    自定义cookie类型
    '''
    def enableCookie(self,cookie_type = None):
        self.cookiejar = cookielib.CookieJar()
        self.opener.add_handler(urllib2.HTTPCookieProcessor(self.cookiejar))

    '''
    TODO
    '''
    def setProxy(self, server, username, password):
        handler = None
        if len(username) != 0 and len(password) != 0:
            handler = None
            #urllib2.ProxyBasicAuthHandler()
            #urllib2.ProxyDigestAuthHandler()
        else:
            handler = urllib2.ProxyHandler({"http" : 'http://127.0.0.1:8080'})

        self.opener.add_handler(handler)
        #self.opener.

    def getResponse(self):
        response = None
        error = None

        try:
            self.request = self.buildRequest(self.url)
            r = self.request.get_selector()
            response = self.opener.open(self.request)

        #有时状态码指出服务器无法完成请求。默认的处理器会为你处理一部分这种应答。
        except urllib2.HTTPError as e:
            error = e
        #URLError在没有网络连接(没有路由到特定服务器)，或者服务器不存在的情况下产生。
        except urllib2.URLError as e:
            error = e

        except Exception as e:
            error = e


        '''
        HTTP Error
        '''

        return response.read(), error

    def buildRequest(self,url):
        request = urllib2.Request(url)
        request.add_header('User-Agent', getRandomAgent())
        return request

'''
self.method=lambda: 'POST'
'''
class MethodGET(Method):
    def __init__(self,url='/'):
        Method.__init__(self)

    def buildRequest(self, url):
        request = Method.buildRequest(self,url)
        request.get_method = lambda: 'GET'
        request.add_header('User-Agent', getRandomAgent())
        return request

'''
Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。常见的取值有：
application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
application/json ： 在 JSON RPC 调用时使用
application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
'''
class MethodPOST(Method):
    def __init__(self):
        Method.__init__(self)
        self.data = None


    def buildRequest(self, url):
        request = Method.buildRequest(self, url)
        request.get_method = lambda: 'POST'
        request.add_data(self.data)
        return request

class MethodPUT(Method):
    def __init__(self,url='/'):
        Method.__init__(self)


    def buildRequest(self, url):
        request = Method.buildRequest(self,url)
        request.get_method = lambda: 'PUT'
        data = 'test'
        request.add_data(data)
        request.add_header('Content-Length', len(data))
        request.add_header('User-Agent', getRandomAgent())
        return request

class MethodOPTIONS(Method):
    def __init__(self,url='/'):
        Method.__init__(self)


    def buildRequest(self, url):
        request = Method.buildRequest(self,url)
        request.get_method = lambda: 'OPTIONS'
        request.add_header('User-Agent', getRandomAgent())
        return request

class MethodHEAD(Method):
    def __init__(self,url='/'):
        Method.__init__(self)


    def buildRequest(self, url):
        request = Method.buildRequest(self,url)
        request.get_method = lambda: 'HEAD'
        return request


class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        pass

class CustomOpener:
    def __init__(self):
        self.opener = urllib2.build_opener()
        self.cookie = cookielib.CookieJar()
        #urllib2.install_opener(opener)#urllib2.urlopen

    def enable_cookie(self):
        cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener.add_handler(cookieHandler)

    def enable_proxy(self):
        proxyHandler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
        self.opener.add_handler(proxyHandler)

    def enable_redirector(self):
        pass

    def open(self, url):
        self.opener.open(url)