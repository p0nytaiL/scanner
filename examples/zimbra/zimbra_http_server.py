
hosts = ''
hosts = hosts.split('\n')

from examples.zimbra.job import *
from examples.zimbra.outputformatter import *

from PackageScanner.Functions.Subnet.HTTPServer.OutputFormatter import *
from PackageScanner.Functions.Subnet.HTTPServer.Job import HTTPHeaderJob, HTTPServerJob
from PackageScanner.Scanner import Scanner_v1


class FindVulnZimbraMailServer(Scanner_v1):
    def __init__(self,  timeout = 5):
        Scanner_v1.__init__(self)
        self._timeout = timeout
        self._outputFormatters.append(OutputFormatterConsoleZimbraLFI())

    def createJobs(self,targets):
        for index, hostname in enumerate(targets):
                self._jobQueue.addJob(JobZimbraLFIDetector(index, hostname))

        return len(targets)

if __name__ == '__main__':
    s = FindVulnZimbraMailServer()
    s._description = 'zimbra'
    s.scan(targets=hosts, thread_count=32)
    for r in s:
        pass
