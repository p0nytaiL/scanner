#!/usr/bin/python
#coding=utf-8
from ToolKits.OnlineDict import *

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Any words you wanner search: '
        exit(1)

    onlinedicts = [OnlineDictBing(), OnlineDictICIBA()]

    for onlinedict in onlinedicts:
        onlinedict.searchWord(sys.argv[1])
    exit(0)