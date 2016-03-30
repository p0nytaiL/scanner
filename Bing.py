#!/usr/bin/python
#coding=utf-8

import sys,optparse

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


    settings, args = parser.parse_args(argv)

    # check number of arguments, verify values, etc.:
    if args:
        parser.error('program takes no command-line arguments;'
                     '"%s" ignored.' % (args,))

    return settings, args

from PackageSearchEngine.SearchEngineBing import *

def main(argv=None):
    settings, args = process_command_line(argv)

    search_engine = SearchEngineBing()
    search_engine.page_parse = PageParseLinks()
    keywords = ''
    if None != settings.ip:
        keywords = 'ip:%s' % (settings.ip)
    elif None != settings.domain:
        keywords = 'domain:%s' % (settings.domain)
    else:
        pass

    results = search_engine.AnalyzeResult(keywords)

    for index, record in enumerate(results):
        print '[%03d]\t%s'%(index+1, record)

if __name__ == '__main__':
    main()