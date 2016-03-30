from PackageScanner.Functions.Subnet.FindHTTPServer import FindHTTPServer
from PackageScanner.Functions.DNS.Domain_v1 import FindSubDomain
from PackageScanner.Functions.Subnet.HTTPServer.Job import HTTPServerJob

class FindDomainHTTPServer(FindHTTPServer):
    def __init__(self):
        FindHTTPServer.__init__(self, ports = [80,443], timeout=5)
        self._dict_name = 'test'

    def createJobs(self,targets):
        s = FindSubDomain()
        s._enable_header = False
        s._enable_footer = False
        s._directory_name = self._dict_name
        s.scan(targets=targets, thread_count= 32)
        valid_hostnames = []
        for job in s:
            if job != None:
                valid_hostnames.append(job.hostname)
                for port in self._ports:
                    self._jobQueue.addJob(HTTPServerJob(len(valid_hostnames), job.hostname, port, self._timeout))

        print valid_hostnames


if __name__ == '__main__':
    s = FindDomainHTTPServer()
    s.scan('github.com', thread_count=32)
    for r in s:
        pass