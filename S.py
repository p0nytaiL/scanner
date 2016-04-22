#!/usr/bin/python
#coding=utf-8

import sys
import socket

import optparse
import netaddr
from PackageScanner.Functions.Subnet.FindHTTPServer import FindHTTPServer, FindHTTPServer1
from PackageScanner.Functions.DNS.Domain_v1 import FindSubDomain
from PackageScanner.Functions.DNS.DomainHTTPServers import FindDomainHTTPServer
from PackageSearchEngine.SearchEngineRobtex import SearchEngineRobtex
from PackageSearchEngine.SearchEngineBing import SearchEngineBing

def process_command_line(argv):
    if argv is None:
        argv = sys.argv[1:]

    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)

    parser.add_option(      # customized description; put --help last
        '-h', '--help', action='help',
        help='Show this help message and exit.')


    parser.add_option("-o", "--outfile", dest="outfile",
                  help="write report to FILE", metavar="FILE")

    parser.add_option("-f", "--function", dest="function",
                  help="scanner class name", metavar="FUNCTION")

    parser.add_option("-t", "--target", dest="target",
                  help="target/targets: domain name(full qualified domain name), subnet, IP...", metavar="TARGET")

    parser.add_option("-d", "--dictionary", dest="dictionary", default='small',
                  help="dictionary name: test, small, large...", metavar="DIRECTORY")

    parser.add_option("-p", "--ports", dest="ports", default='',
                  help="--ports=80,81,8080...", metavar="PORTS")

    '''
    parser.add_option("-t", "--timeout", dest="timeout", default=3,
                  help="global socket timeout", metavar="TIMEOUT")
    '''

    parser.add_option("-n", "--threadcount", dest="threadcount", default=32,
                  help="scan thread count", metavar="THREADCOUNT")

    settings, args = parser.parse_args(argv)

    # check number of arguments, verify values, etc.:
    if args:
        parser.error('program takes no command-line arguments;'
                     '"%s" ignored.' % (args,))

    return settings, args

global_timeout = 5

def main(argv=None):
    settings, args = process_command_line(argv)
    scanner = None
    target = None
    function = settings.function
    #C段http主机扫描
    if function == 'subnet-httpserver':
        target = netaddr.IPNetwork(settings.target)
        target_ports = []
        if len(settings.ports) != 0:
            ports = settings.ports.split(',')
            for port in ports:
                target_ports.append(int(port))

        scanner = FindHTTPServer(ports=target_ports, timeout= global_timeout)
        scanner._description = str(target.network)

    #c段ptr记录反查
    elif function == 'subnet-robtex':
        socket.setdefaulttimeout(global_timeout)
        search_engine = SearchEngineRobtex()
        #https://www.robtex.com/route/192.168.0.1-24.html
        search_engine.url = 'https://www.robtex.com/route/' + settings.target.replace('/','-') + '.html'
        scanner = FindHTTPServer1(ports = [80,443], timeout= global_timeout)
        scanner._description = 'robtex'
        target = search_engine.AnalyzeResult('')

    #二级域名http主机扫描(来自二级域名爆破结果)
    elif function == 'subdomain-httpserver':
        socket.setdefaulttimeout(global_timeout)
        scanner = FindDomainHTTPServer()
        scanner._description = settings.target
        scanner._dict_name = settings.dictionary
        target = settings.target

    #二级域名爆破
    elif function == 'subdomain-dns':
        socket.setdefaulttimeout(global_timeout)
        scanner = FindSubDomain()
        scanner._description = settings.target
        scanner._directory_name = settings.dictionary
        target = settings.target

    #二级域名bing接口
    elif function == 'subdomain-bing':
        socket.setdefaulttimeout(global_timeout)
        search_engine = SearchEngineBing()
        keywords = 'domain:%s' % (settings.target)
        results = search_engine.AnalyzeResult(keywords)

        scanner = FindHTTPServer1(ports = [80,443],timeout= global_timeout)
        scanner._description = settings.target
        target = results

    #旁站查询,bing搜索结果
    elif function == 'virtualhost-bing':
        socket.setdefaulttimeout(global_timeout)
        search_engine = SearchEngineBing()
        keywords = 'ip:%s' % (settings.target)
        results = search_engine.AnalyzeResult(keywords)

        scanner = FindHTTPServer1(ports = [80,443], timeout= global_timeout)
        scanner._description = settings.target
        target = results

    #elif function == 'targetsubdomain':
    #    socket.setdefaulttimeout(global_timeout)
    #    scanner = FindTargetSubDomain()
    #    target = settings.target

    elif function == 'domainservers':
        print 'not impl'
        exit(-1)

    elif function == 'news':
        print 'not impl'
        exit(-1)

    else:
        print 'unsupport function: %s' % (settings.function)
        exit(-1)
    import datetime
    starttime = datetime.datetime.now()
    try:
        count_jobs = scanner.scan(targets = target, thread_count= int(settings.threadcount))
        for index,result in enumerate(scanner):
            pass

    except KeyboardInterrupt as e1:
       print "\rFinishing pending requests..."
       scanner.stop()
       return -1

    except Exception as e:
        scanner.stop()
        print 'main' + e

    #long running
    endtime = datetime.datetime.now()
    print 'Time consuming: ',(endtime - starttime).seconds,'s'
    return 0        # success


if __name__ == '__main__':
    main()
