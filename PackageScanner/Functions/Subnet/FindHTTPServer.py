#!/usr/bin/python
#coding=utf-8


from PackageScanner.Functions.Subnet.HTTPServer.OutputFormatter import *
from PackageScanner.Functions.Subnet.HTTPServer.Job import HTTPHeaderJob
from PackageScanner.Scanner import Scanner_v1


class FindHTTPServer(Scanner_v1):
    def __init__(self, ports = [80,81,82,83,84,85,86,87,88,89,90,311,383,443,591,593,631,901,1220,1414,1741,1830,2301,2381,2809,3037,3057,3128,3443,3702,4343,4848,5250,6080,6988,7000,7001,7007,7144,7145,7510,7777,7779,8000,8008,8014,8028,8080,8085,8088,8090,8118,8123,8180,8181,8222,8243,8280,8300,8500,8800,8888,8899,9000,9060,9080,9090,9091,9443,9999,10000,11371,34443,34444,41080,50000,50002,55555]):
        Scanner_v1.__init__(self)
        self._ports = ports
        self._outputFormatters.append(OutputFormatterConsoleHTTPServer())
        self._outputFormatters.append(OutputFormatterFileHTTPServer())

    def createJobs(self,targets):
        for index1, port in enumerate(self._ports):
            for index2, ip in enumerate(targets):
                if targets.size > 1 and ip in [targets.network, targets.broadcast]:
                    continue
                self._jobQueue.addJob(HTTPHeaderJob(((index1) * len(targets))+(index2+1), str(ip), port))

        return len(self._ports) * len(targets)


if __name__ == '__main__':
    import socket
    socket.setdefaulttimeout(3)
    s = FindHTTPServer(ports=[80,81,82,83,8000,8001,8002,8003,8080,8088])
    import netaddr
    net = netaddr.IPNetwork('118.193.216.0/24')
    s._description = str(net.network)
    s.scan(targets=net, thread_count= 32)
    for r in s:
        pass