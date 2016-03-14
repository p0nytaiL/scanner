#!/usr/bin/python
#coding=utf-8

import sys
import socket

import optparse
import netaddr
from PackageScanner.Functions.Subnet.FindHTTPServer import FindHTTPServer
from PackageScanner.Functions.DNS.Domain_v1 import FindSubDomain
from PackageScanner.Functions.DNS.TargetDomain import FindTargetSubDomain

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


def main(argv=None):
    settings, args = process_command_line(argv)
    socket.setdefaulttimeout(3)

    scanner = None
    target = None
    function = settings.function
    if function == 'findhttpserver':
        target = netaddr.IPNetwork(settings.target)
        target_ports = []
        if len(settings.ports) == 0:
            target_ports = [80,81,82,83,84,85,86,87,88,89,90,311,383,443,591,593,631,901,1220,1414,1741,1830,2301,2381,2809,3037,3057,3128,3443,3702,4343,4848,5250,6080,6988,7000,7001,7007,7144,7145,7510,7777,7779,8000,8008,8014,8028,8080,8085,8088,8090,8118,8123,8180,8181,8222,8243,8280,8300,8500,8800,8888,8899,9000,9060,9080,9090,9091,9443,9999,10000,11371,34443,34444,41080,50000,50002,55555]
        else:
            ports = settings.ports.split(',')
            for port in ports:
                target_ports.append(int(port))

        scanner = FindHTTPServer(ports=target_ports)
        scanner._description = str(target.network)

    elif function == 'findsubdomain':
        scanner = FindSubDomain()
        scanner._description = settings.target
        scanner._directory_name = settings.dictionary
        target = settings.target

    elif function == 'targetsubdomain':
        scanner = FindTargetSubDomain()
        target = settings.target

    elif function == 'domainservers':
        print 'not impl'
        exit(-1)
    elif function == 'news':
        print 'not impl'
        exit(-1)
    else:
        print 'unsupport function: %s' % (settings.function)
        exit(-1)
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

    return 0        # success


if __name__ == '__main__':
    main()
