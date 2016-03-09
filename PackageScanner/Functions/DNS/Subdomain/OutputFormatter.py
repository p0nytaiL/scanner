#!/usr/bin/python
#coding=utf-8


from PackageScanner.OutputFormatter import *
import netaddr

class IPCollection:
    def __init__(self):
        self._ip_networks = []

    def add(self, ip):
        self._ip_networks.append(netaddr.IPNetwork(ip))

    def getSubnets(self):
        return netaddr.cidr_merge(self._ip_networks)

ip_collection = IPCollection()

class OutputFormatterConsoleSubdomain(OutputFormatterConsole):
    def __init__(self):
        OutputFormatterConsole.__init__(self)
        self.nsrecords=[]

    def printResult(self, report_object):
        if report_object.result == None or len(report_object.result) == 0:
            return None

        print '\r',report_object.hostname,'@',report_object.current_nameserver
        for ns_record in report_object.result:
            ip_collection.add(ns_record['address'])
            print '\r\t' , ns_record['type'], ns_record['address']

        return None

    def printHeader(self, description):
        print "==============="
        print " subdomain of %s" % (description)
        print "==============="
        pass

    def printFooter(self, description):
        if len(ip_collection._ip_networks) != 0:
            print '\r\nIP Address Range Summary:'
            for subnet in ip_collection.getSubnets():
                print subnet


class OutputFormatterFileSubdmamin(OutputFormatterFile):
    def __init__(self):
        OutputFormatterFile.__init__(self)

    def printHeader(self, description):
        OutputFormatterFile.printHeader(self, description)
        self._fileHandle.write('<html><header>')
        self._fileHandle.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">')
        self._fileHandle.write('</header>')
        self._fileHandle.write('<body><table border frame=box>')
        self._fileHandle.write("<tr><td>hostname</td><td>resource records</td></tr>")

    def printResult(self, job):
        if job.result == None or len(job.result) == 0:
            return None
        self._fileHandle.write('<tr>')
        self._fileHandle.write(('<td>http://%s</td>' % (job.hostname)))
        self._fileHandle.write('<td>')
        for rr in job.result:
            self._fileHandle.write(rr['type'])
            self._fileHandle.write('\t')
            self._fileHandle.write(rr['address'])
            self._fileHandle.write('<br/>')
        self._fileHandle.write('</td>')
        self._fileHandle.write('<tr>')

    def printFooter(self, description):
        self._fileHandle.write("</table></body></html>")
        OutputFormatterFile.printFooter(self, description)



class OutputFormatterNextSubdomain(OutputFormatterNext):
    def __init__(self):
        OutputFormatterNext.__init__(self)
        self._ip_address = set()

    def printResult(self, job):
        if job.result == None or len(job.result) == 0:
            return None

        ret = []
        for ns_record in job.result:
            s1 = set()
            s1.add(ns_record['address'])
            if s1.issubset(self._ip_address):
                continue

            #print job.hostname, ns_record['address']
            self._ip_address.add(ns_record['address'])
            ret.append(ns_record['address'])

        return ret

    def printFooter(self, description):
        pass

    def printHeader(self, description):
        pass


if __name__ == '__main__':
    s1 = set()
    s1.add('123456')
    print s1