#!/usr/bin/python
#coding=utf-8

from PackageHTTP.Methods import *
from PackageScanner.JobQueue import Job


class HTTPHeaderJob(Job):
    def __init__(self, id, hostname, port = 80):
        Job.__init__(self, id)
        self.hostname = hostname
        self.port = port
        self.description = '%s:%d'%(hostname, port)

    def do(self):
        self.result = dict.fromkeys(['response_head','error_head',
                                'response_options','error_options',
                                'response_body','error_body',
                                'response_robots', 'error_robots'])

        #任何一个请求(head,options,body,robotx)超时,该job都会被判定为超时
        #二次请求中,如果job中包含上次请求的结果,则不再请求
        #结果打印中不能单纯依据job.exception中是否包含异常来判定该job是该输出
        #应逐个判定response_xxx, error_xxx来输出结果
        #head请求为Job的第一个请求,如果该请求结果非空,则判定当前job为有效job
        try:
            m = None
            #head
            if None == self.result['response_head'] and self.result['error_head'] == None:
                m = HTTPMethodHEAD()
                m.setHostInfo(hostname = self.hostname, port=self.port)
                self.result['response_head'], self.result['error_head'] = m.getResponse()

            #options
            if None == self.result['response_options'] and self.result['error_options'] == None:
                m = HTTPMethodOPTIONS()
                m.setHostInfo(hostname = self.hostname, port=self.port)
                self.result['response_options'], self.result['error_options'] = m.getResponse()

            #body content
            if None == self.result['response_body'] and self.result['error_body'] == None:
                m = HTTPMethodGETPage()
                m.setHostInfo(hostname = self.hostname, port=self.port)
                self.result['response_body'], self.result['error_body'] = m.getResponse()

            #robots
            if None == self.result['response_robots'] and self.result['error_robots'] == None:
                m = HTTPMethodGETRobots()
                m.setHostInfo(hostname = self.hostname, port=self.port)
                self.result['response_robots'], self.result['error_robots'] = m.getResponse()

            #无法判定是请求超时,还是服务器关闭导致的超时
            count_timeout = 0
            exceptions = [self.result['error_head'], self.result['error_options'], self.result['error_body'], self.result['error_robots']]
            for exception in exceptions:
                if isinstance(exception, socket.timeout):
                    count_timeout = count_timeout + 1

            if count_timeout == 4:
                self.is_timeout = True
                self.retry = 3
                self.exception = socket.timeout
                raise socket.timeout

        except Exception as e:
            self.exception = e

        return Job.do(self)

from PackageScanner.JobQueue import Job
import requests
from requests.packages.urllib3.exceptions import *
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

class HTTPServerJob(Job):
    def __init__(self, id, hostname, port = 80, timeout = 5):
        Job.__init__(self, id)
        self.timeout = timeout
        self.hostname = hostname
        self.port = port
        self.scheme = 'http'
        if self.port in [443, 8443, 9443]:
            self.scheme = 'https'
        self.description = '%s:%d'%(hostname, port)

    #优化为一个Session
    def do(self):
        try:
            uri_root = urlparse.urlunsplit((self.scheme,self.description, '/','',''))
            headers = {'User-Agent':getRandomAgent()}
            self.result = {
                #'response_head' : requests.Request('HEAD', uri_root ,headers=headers),
                #'response_robots' : requests.Request('GET', uri_root ,headers=headers),
                'response_get' : requests.Request('GET', uri_root ,headers=headers),
                'response_options' : requests.Request('OPTIONS', uri_root ,headers=headers)
            }

            http_session = requests.Session()

            for k, v in self.result.items():
                request = http_session.prepare_request(v)
                try:
                    self.result[k] = http_session.send(request,
                                                       timeout = self.timeout,
                                                       verify = False)
                except Exception as e:
                    self.result[k] = e

            #超时,连接重置判定
            cnt_exception = 0
            for k, v in self.result.items():
                if not isinstance(v, requests.Response):
                    cnt_exception = cnt_exception + 1

            if cnt_exception == len(self.result):
                self.is_timeout = True
                self.retry = 3
                raise Exception('time out or connection reset')

        except Exception as e:
            self.exception = e

        return Job.do(self)

if __name__ == '__main__':
    job = HTTPServerJob(id=1, hostname='121.40.55.211')
    job.do()
    print job.result