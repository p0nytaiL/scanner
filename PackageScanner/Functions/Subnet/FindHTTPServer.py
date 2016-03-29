#!/usr/bin/python
#coding=utf-8


from PackageScanner.Functions.Subnet.HTTPServer.OutputFormatter import *
from PackageScanner.Functions.Subnet.HTTPServer.Job import HTTPHeaderJob
from PackageScanner.Scanner import Scanner_v1


'''
导致Scanner Result Summary中timeout数量与实际扫描出的结果数量和与总任务数不匹配的原因
扫描失败后,timeout类型记录进timeout队列,[Errno 61] Connection refused 没有记录进timeout队列
'''
vul_ports = [
             80,81,82,83,84,85,86,87,88,89,90,91, #comm http ports
             800,900,
             1220,      #Quick time http server
             2301,2381, #HP HTTP/HTTPS
             3443,      #HP OpenView Network Node Manager WEB Server
             4343,      #WebSEAL, Trend Micro OfficeScan
             4848,      #GlassFish
             6080,      #BigAnt Messenger IM Server
             7001,      #WebLogic Server's HTTP server
             7002,
             7007,
             7510,      #HP OpenView Application Server
             7777,      #Oracle 9i Portal - Apache HTTP (default)
             8001,8002,8003,8004,8005,8006,8007,8008,
             8008,      #IBM HTTP Server administration default
             8009,8010,
             8020,8030,8040,8050,8086,8070,8080,
             8081,8082,8083,8084,8085,8086,8087,8088,8089,
             8090,
             8100,
             8200,
             8300,
             8222,8333,  #VMware Server Management User Interface
             8400,
             8500,      #Macromedia ColdFusion MX Server
             8600,
             8700,
             8800,8890,8879,8888,
             8900,
             9000,9001,9002,9009,
             9060,9080,9443,    #WebSphere Application Server Administration Console
             10000              #Webmin Admin
             ]

class FindHTTPServer(Scanner_v1):
    def __init__(self, ports = vul_ports):
        Scanner_v1.__init__(self)
        if len(ports) == 0:
            ports = vul_ports
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
    target_ports = [80,81,82,83,84,85,86,87,88,89,90,311,383,443,591,593,631,901,1220,1414,1741,1830,2301,2381,2809,3037,3057,3128,3443,3702,4343,4848,5250,6080,6988,7000,7001,7007,7144,7145,7510,7777,7779,8000,8008,8014,8028,8080,8085,8088,8090,8118,8123,8180,8181,8222,8243,8280,8300,8500,8800,8888,8899,9000,9060,9080,9090,9091,9443,9999,10000,11371,34443,34444,41080,50000,50002,55555]
    target_ports = [80]
    s = FindHTTPServer(ports=target_ports)
    import netaddr
    net = netaddr.IPNetwork('127.0.0.1')
    s._description = str(net.network)
    s.scan(targets=net, thread_count= 1)
    for r in s:
        pass