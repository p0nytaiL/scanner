#!/usr/bin/python
#coding=utf-8

import requests
from PackageScanner.OutputFormatter import *
from PackageHTTP.Body import *

class ResponseZimbraLFI(HTTPBodyResponseText):
    def __init__(self, body, encoding):
        HTTPBodyResponseText.__init__(self, body, encoding)
        self.exploit_keyword = 'ldap_root_password'

    def is_exploite(self):
        ok = False;
        try:
            self.body = self.body.decode(self.encoding)
            if self.body.find(self.exploit_keyword) != -1:
                ok = True
        except Exception as e:
            ok = False

        return ok

class OutputFormatterConsoleZimbraLFI(OutputFormatterConsole):
    def __init__(self):
        OutputFormatterConsole.__init__(self)

    def printResult(self, job):
        for k, response in job.result.items():
            if isinstance(response,requests.Response):
                if k in ('http', 'https'):
                    body = ResponseZimbraLFI(response.content, get_requests_response_encoding(response))
                    if body.is_exploite():
                        print 'Detect Exploited Zimbra Mail Service on %s://%s' % (k, job.description)
                if k in ('http_mgr','https_mgr'):
                    if response.status_code == '200':
                        print 'Detect Zimbra MailAdmin Service on %s://%s' % (k, job.description)


