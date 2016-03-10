#!/usr/bin/python
#coding=utf-8


from PackageScanner.Functions.Subnet.HTTPServer.OutputFormatter import *
from PackageScanner.Functions.Subnet.HTTPServer.Job import HTTPHeaderJob
from PackageScanner.Scanner import Scanner_v1

'''
导致Scanner Result Summary中timeout数量与实际扫描出的结果数量和与总任务数不匹配的原因
扫描失败后,timeout类型记录进timeout队列,[Errno 61] Connection refused 没有记录进timeout队列
'''

class FindHTTPServer(Scanner_v1):
    def __init__(self, ports):
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
    s = FindHTTPServer(ports=[80])
    import netaddr
    net = netaddr.IPNetwork('192.168.1.1/24')
    s._description = str(net.network)
    s.scan(targets=net, thread_count= 32)
    for r in s:
        pass