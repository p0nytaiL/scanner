#!/usr/bin/python
#coding=utf-8

import sys
import socket

import optparse
import netaddr
from PackageScanner.Functions.Subnet.HTTPServer import FindHTTPServer
from PackageScanner.Functions.DNS.Domain_v1 import FindSubDomain

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
                  help="target/targets: dictionary name...", metavar="TARGET")

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
        scanner = FindHTTPServer()
        scanner._description = str(target.network)

    elif function == 'findsubdomain':
        scanner = FindSubDomain()
        scanner._description = settings.target
        scanner._directory_name = settings.dictionary
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
