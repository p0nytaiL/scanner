#!/usr/bin/python
#coding=utf-8
import sys,optparse

from PackageSearchEngine.SearchEnginePacketStorm import *

def process_command_line(argv):
    if argv is None:
        argv = sys.argv[1:]

    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)

    parser.add_option(      # customized description; put --help last
        '-h', '--help', action='help',
        help='Show this help message and exit.')


    parser.add_option("-q", "--query", dest="query",
                  help="query string", metavar="QUERY")


    settings, args = parser.parse_args(argv)

    # check number of arguments, verify values, etc.:
    if args:
        parser.error('program takes no command-line arguments;'
                     '"%s" ignored.' % (args,))

    return settings, args

def main(argv=None):
    settings, args = process_command_line(argv)
    s = None
    if settings.query == None:
        s = SearchEnginePacketStromToday()
    else:
        s = SearchEnginePacketStromSearch()

    echoResults(s.AnalyzeResult(settings.query))


if __name__ == '__main__':
    main()