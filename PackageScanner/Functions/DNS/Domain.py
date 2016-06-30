#!/usr/bin/python
#coding=utf-8

import socket

from PackageScanner.JobQueue import Job
from PackageScanner.OutputFormatter import OutputFormatter
from PackageScanner.Scanner import Scanner_v1
from PackageScanner.TargetLoader import TargetLoader

#通过getaddrinfo方法获取ip地址
#泛解析地址
nslookup_error_ip_addresses=['1.1.1.1']

class SubDomainJob(Job):
    def __init__(self,id, hostname, ports):
        Job.__init__(self,id)
        self.hostname = hostname
        self.ports = ports

    def filterNSRecords(self, nsrecords):
        ip = []
        for nsrecord in nsrecords:
            if nsrecord[4][0] in nslookup_error_ip_addresses:
                continue
            else:
                ip.append(nsrecord[4][0])

        return ip

    def do(self):
        result = {
            'hostname' : self.hostname,
            'nsrecords' : None,
            'exceptions' : [],
            'exec_time':0
        }
        try:
            #start = time()
            result['nsrecords'] = self.filterNSRecords(socket.getaddrinfo(self.hostname, 0, socket.AF_INET,socket.SOCK_STREAM))

        except socket.gaierror as e1:
            if e1.errno == 8: result['nsrecords'] = None

        except Exception as e:
            result['exceptions'].append(e)

        #result['exec_time'] = (time()-start)
        return result


class OutputFormatterSubDomainRecord(OutputFormatter):
    def __init__(self):
        OutputFormatter.__init__(self)
        self.nsrecords=[]

    def printResult(self, report_object):
        if report_object['nsrecords'] != None and len(report_object['nsrecords']) > 0:
            print '\r' + report_object['hostname'], report_object['nsrecords']
            self.nsrecords.extend(report_object['nsrecords'])

        print '\r' + report_object['hostname'],
        import sys
        sys.stdout.flush()

    def printHeader(self, description):
        print "==============="
        print " subdomain of %s" % (description)
        print "==============="
        pass

    def printFooter(self, description):
        self.nsrecords = list(set(self.nsrecords))
        self.nsrecords.sort()
        print '\r\nIP Address Range Summary:'
        for ip in self.nsrecords:
            print ip

class FindSubDomain(Scanner_v1):
    def __init__(self):
        Scanner_v1.__init__(self)
        self._outputFormatter = OutputFormatterSubDomainRecord()
        self.domain_prefix_list = []

    def loadSubdomainDict(self):
        from os import path
        target_loader = TargetLoader()
        self.domain_prefix_list = target_loader.loadTargets(file=path.dirname(__file__) + '/dict/small')
        self.domain_prefix_list = list(self.domain_prefix_list)
        self.domain_prefix_list.sort()

    def createJobs(self,targets):
        self.loadSubdomainDict()
        domain = targets
        self._description = targets
        for index, domain_prefix in enumerate(self.domain_prefix_list):
            domain_name = '%s.%s'%(domain_prefix, domain)
            self._jobQueue.addJob(SubDomainJob(index+1, domain_name, [80]))

        return len(self.domain_prefix_list)

if __name__ == '__main__':
    s = FindSubDomain()
    s.scan(targets='transas.com', thread_count= 32)
    for r in s:
        pass