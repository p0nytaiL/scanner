#!/usr/bin/python
#coding=utf-8

import sys,optparse
from PackageScanner.Functions.Subnet.FindHTTPServer import FindHTTPServer1

def process_command_line(argv):
    if argv is None:
        argv = sys.argv[1:]

    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)

    parser.add_option(      # customized description; put --help last
        '-h', '--help', action='help',
        help='Show this help message and exit.')


    parser.add_option("-i", "--ip", dest="ip",
                  help="ip address", metavar="IP")

    parser.add_option("-d", "--domain", dest="domain",
                  help="domain", metavar="DOMAIN")

    parser.add_option("-b", "--banner", dest="banner",
                  help="banner", metavar="BANNER")

    settings, args = parser.parse_args(argv)

    # check number of arguments, verify values, etc.:
    if args:
        parser.error('program takes no command-line arguments;'
                     '"%s" ignored.' % (args,))

    return settings, args

from PackageSearchEngine.SearchEngineBing import *

def printResult(results):
    for i, r in enumerate(results):
        print '[%03d] %s' % (i, r)

def printHTTPResult(results, keywords):
    try:
        scanner = FindHTTPServer1(ports=[80, 443])
        scanner._description = keywords
        scanner.scan(targets=results, thread_count=32)
        for r in scanner:
            pass

    except KeyboardInterrupt as e1:
       print "\rFinishing pending requests..."
       scanner.stop()
       return -1

    except Exception as e:
        scanner.stop()
        print 'main' + str(e)

def main(argv=None):
    settings, args = process_command_line(argv)

    search_engine = SearchEngineBing()
    keywords = ''
    description = ''
    if None != settings.ip:
        keywords = 'ip:%s' % (settings.ip)
        description = settings.ip
    elif None != settings.domain:
        keywords = 'domain:%s' % (settings.domain)
        description = settings.domain
    else:
        pass

    results = search_engine.AnalyzeResult(keywords)

    if None != settings.banner:
        printHTTPResult(results, description)
    else:
        printResult(results)

if __name__ == '__main__':
    main()