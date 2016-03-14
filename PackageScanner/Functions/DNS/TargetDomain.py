#!/usr/bin/python
#coding=utf-8


from PackageScanner.Scanner import Scanner_v1
from PackageThread.JobQueue import Job
from PackageScanner.TargetLoader import TargetLoader
from PackageScanner.Functions.DNS.Domain_v1 import FindSubDomain
from PackageScanner.OutputFormatter import *

class OutputFormatterConsoleTargetDomain(OutputFormatterConsole):
    def __init__(self):
        OutputFormatterConsole.__init__(self)

    def printHeader(self, description):
        pass

    def printFooter(self, description):
        pass

    def printResult(self, job):
        pass

class TargetDomainJob(Job):
    def __init__(self, id, target):
        Job.__init__(self, id)
        self._target = target
        self._scanner = FindSubDomain()

    def do(self):
        self._scanner.scan(targets=self._target, thread_count=32)
        for r in self._scanner:
            pass

        return Job.do()

class FindTargetSubDomain(Scanner_v1):
    def __init__(self):
        Scanner_v1.__init__(self)
        self._targets = ''
        self._outputFormatters.append(OutputFormatterConsoleTargetDomain())

    def loadTargets(self, targets):
        t = TargetLoader()
        self._targets = targets
        return t.loadTargets(file = self._targets)

    def createJobs(self, targets):
        domains = self.loadTargets(targets)
        self._description = domains
        for index, domain in enumerate(domains):
            self._jobQueue.addJob(TargetDomainJob(index+1, domain))

        return len(domain)


if __name__ == '__main__':
    s = FindTargetSubDomain()
    import os.path
    targets = os.path.dirname(__file__) + '/' + 'targets.txt'
    s.scan(targets=targets, thread_count=1)
    for r in s:
        pass