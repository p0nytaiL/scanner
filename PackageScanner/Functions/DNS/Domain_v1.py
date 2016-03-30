#!/usr/bin/python
#coding=utf-8

import Queue

from PackageScanner.Functions.DNS.Subdomain.OutputFormatter import *
from PackageScanner.Functions.DNS.Subdomain.Job import *
from PackageScanner.Scanner import Scanner_v1
from PackageScanner.TargetLoader import TargetLoader

class FindSubDomain(Scanner_v1):
    def __init__(self):
        Scanner_v1.__init__(self)
        self._outputFormatters.append(OutputFormatterConsoleSubdomain())
        self._outputFormatters.append(OutputFormatterFileSubdmamin())
        self._outputFormatters.append(OutputFormatterNextSubdomain())
        self._directory_name = 'small'

    def loadSubdomainDict(self):
        from os import path
        target_loader = TargetLoader()
        domain_prefixes = target_loader.loadTargets(file=path.dirname(__file__) + '/dict/' + self._directory_name)
        domain_prefixes = list(domain_prefixes)
        domain_prefixes.sort()
        return domain_prefixes

    def createJobs(self,targets):
        r = resolver()
        nameservers = r.get_authoritative(hostname=targets)
        queue_nameservers = Queue.Queue()
        for ns in nameservers:
            queue_nameservers.put([ns])
        if queue_nameservers.qsize() == 0:
            raise Exception("Can`t find Auth DNS ervers")
        '''
        nameservers = CheckHostJob.recursion_reuqest_ns_record(targets)

        for ns,ns_records in nameservers.items():
            for ns_record in ns_records:
                #AAAA记录不参与扫描
                if ns_record['type']=='A':
                    queue_nameservers.put([ns_record])
        '''
        domain_prefixes = self.loadSubdomainDict()
        domain = targets
        self._description = targets
        for index, domain_prefix in enumerate(domain_prefixes):
            hostname = '%s.%s'%(domain_prefix, domain)
            self._jobQueue.addJob(CheckHostJob(index+1, hostname, queue_nameservers))

        return len(domain_prefixes)





if __name__ == '__main__':
    s = FindSubDomain()
    s._directory_name = 'test'
    s.scan(targets='google.com', thread_count= 16)
    valid_hostnames = []
    for r in s:
        if r != None:
            valid_hostnames.append(r.hostname)

    print valid_hostnames
