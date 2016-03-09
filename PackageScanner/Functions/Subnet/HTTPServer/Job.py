#!/usr/bin/python
#coding=utf-8

from PackageThread.JobQueue import Job
from PackageHTTP.Methods import *

class HTTPHeaderJob(Job):
    def __init__(self, id, hostname, port = 80):
        Job.__init__(self, id)
        self.hostname = hostname
        self.port = port

    def do(self):
        self.result = dict.fromkeys(['response_head','error_head',
                                'response_options','error_options',
                                'response_body','error_body',
                                'response_robots', 'error_robots'])
        try:
            #head
            m = HTTPMethodHEAD()
            m.setHostInfo(hostname = self.hostname, port=self.port)
            self.result['response_head'], self.result['error_head'] = m.getResponse()

            #options
            m = HTTPMethodOPTIONS()
            m.setHostInfo(hostname = self.hostname, port=self.port)
            self.result['response_options'], self.result['error_options'] = m.getResponse()

            #body content
            m = HTTPMethodGETPage()
            m.setHostInfo(hostname = self.hostname, port=self.port)
            self.result['response_body'], self.result['error_body'] = m.getResponse()

            #robots
            m = HTTPMethodGETRobots()
            m.setHostInfo(hostname = self.hostname, port=self.port)
            self.result['response_robots'], self.result['error_robots'] = m.getResponse()

            print '\r%s:%d'%(self.hostname,self.port),

        except socket.timeout as e1:
            self.is_timeout = True
            self.retry = 3

        except Exception as e:
            self.exception = e

        return Job.do(self)