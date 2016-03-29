#!/usr/bin/python
#coding=utf-8


from PackageScanner.OutputFormatter import *

class OutputFormatterConsoleHTTPServer(OutputFormatterConsole):
    def __init__(self):
        pass

    def printHeader(self, description):
        print '---------------------------------------------------------------------------------------------------------'
        print '%15s%040s'%('HOST', 'TITLE')
        print '---------------------------------------------------------------------------------------------------------'

    #Print Title
    def printResult(self, job):
        if job.exception != None:
            #print '\r%s:%d\t'%(result.hostname, result.port), result.exception
            return None
        try:
            print '\r',('%s:%d' % (job.hostname,job.port)),('%80s'%(job.result['response_body']['title']))
        except:
            print job.hostname, job.port

    def printFooter(self, description):
        print '\r---------------------------------------------------------------------------------------------------------'
        print '%15s%040s'%('HOST', 'TITLE')
        print '---------------------------------------------------------------------------------------------------------'


class OutputFormatterFileHTTPServer(OutputFormatterFile):
    def __init__(self):
        OutputFormatterFile.__init__(self)
        self._index = 1

    def printFilterHeader(self, headers):
        if headers == None:
            print 'None'

        filter = [
            'accept-ranges',
            'etag',
            'date',
            'content-length',
            'content-type',
            'connection',
            'transfer-encoding',
            'last-modified',
            'expires',
            'pragma',
            'cache-control',
            'set-cookie',
            'vary',
            'content-encoding',
            'content-language',
            'keep-alive'
        ]
        for header_name, header_value in headers.items():
            if header_name.lower() in filter:   continue
            self._fileHandle.write(header_name + ': ' + header_value +'<br/>')

    def printHeader(self, description):
        self._fileExt = '.html'
        OutputFormatterFile.printHeader(self, description)
        if self._fileHandle != None:
            self._fileHandle.write('<html><head>' \
              '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">' \
              '<style type="text/css">' \
              'table {' \
              'width: 100%;' \
              'table-layout: fixed;' \
              'word-wrap: break-word;' \
              '}' \
              '</style>' \
              '</head>' \
              '<table border frame=box>' \
              '<tr>' \
              '<td style="width: 4%;">' \
              'id' \
              '</td>' \
              '<td style="width: 16%;">' \
              'host' \
              '</td>' \
              '<td style="width: 10%;">' \
              'title' \
              '</td>' \
              '<td style="width: 20%;">' \
              'HEAD response' \
              '</td>' \
              '<td style="width: 20%;">' \
              'OPTIONS response'\
              '</td>' \
              '</td>' \
              '<td style="width: 20%;">' \
              'Robots.txt'\
              '</td>' \
              '</tr>')

    def printResult(self,job):
        # echo to html file
        if job.exception is not None:
            self._fileHandle.write('<!-- %s:%d %s-->' %(job.hostname, job.port, job.exception))
            return False

        self._fileHandle.write('<tr>')
        self._fileHandle.write('<td>%s</td>' % (self._index))
        self._index = self._index + 1

        url = 'http://%s:%d' % (job.hostname, job.port)
        self._fileHandle.write('<td> <a href=%s>%s</a> </td>' % (url, url))

        #body content
        self._fileHandle.write('<td>')
        try:
            if job.result['error_body'] is not None:
                self._fileHandle.write(str(job.result['error_body']))
            else:
                self._fileHandle.write('%s' % (job.result['response_body']['title']))
            self._fileHandle.write('</td>')
        except Exception as e:
            self._fileHandle.write(str(e))
        #head
        self._fileHandle.write('<td>')
        try:
            if job.result['error_head'] is not None:
                self._fileHandle.write(str(job.result['error_head']))
            else:
                self._fileHandle.write('status %s<br/>' % (job.result['response_head']['status']))
                self.printFilterHeader(job.result['response_head']['headers'])
        except Exception as e:
            self._fileHandle.write(str(e))
        self._fileHandle.write('</td>')

        #option
        self._fileHandle.write('<td>')
        try:
            if job.result['error_options'] is not None:
                self._fileHandle.write(str(job.result['error_options']))
            else:
                self._fileHandle.write('status %s<br/>' % (job.result['response_options']['status']))
                self.printFilterHeader(job.result['response_options']['headers'])
        except Exception as e:
            self._fileHandle.write(str(e))
        self._fileHandle.write('</td>')

        #robots
        self._fileHandle.write('<td>')
        try:
            if job.result['error_robots'] is not None:
                self._fileHandle.write(str(job.result['error_robots']))
            else:
                self._fileHandle.write(job.result['response_robots']['body'].replace('\n','<br/>'))
        except Exception as e:
            self._fileHandle.write(str(e))

        self._fileHandle.write('</td>')
        self._fileHandle.write('</tr>')

        return False

    def printFooter(self, description):
        if self._fileHandle != None:
            self._fileHandle.write('</table></html>')
        OutputFormatterFile.printFooter(self, description)


import requests
from PackageHTTP.Body import HTTPBodyResponse

class OutputFormatterConsoleHTTPServer1(OutputFormatterConsoleHTTPServer):
    def __init__(self):
        OutputFormatterConsoleHTTPServer.__init__(self)

    def printResult(self, job):
        response = job.result['response_get']

        if isinstance(response,requests.Response):
            body = HTTPBodyResponse(response.content, response.apparent_encoding)
            print  '\r',job.description, '\t'*6, body.title


class OutputFormatterFileHTTPServer1(OutputFormatterFileHTTPServer):
    def __init__(self):
        OutputFormatterFileHTTPServer.__init__(self)

    def printHeader(self, description):
        self._fileExt = '.html'
        OutputFormatterFile.printHeader(self, description)
        if self._fileHandle != None:
            self._fileHandle.write('<html><head>' \
              '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">' \
              '<style type="text/css">' \
              'table {' \
              'width: 100%;' \
              'table-layout: fixed;' \
              'word-wrap: break-word;' \
              '}' \
              '</style>' \
              '</head>' \
              '<table border frame=box>' \
              '<tr>' \
              '<td style="width: 3%;">' \
              'id' \
              '</td>' \
              '<td style="width: 17%;">' \
              'host' \
              '</td>' \
              '<td style="width: 20%;">' \
              'title' \
              '</td>' \
              '<td style="width: 30%;">' \
              'informations' \
              '</td>' \
              '<td style="width: 25%;">' \
              'OPTIONS'\
              '</td>' \
              '<td style="width: 5%;">' \
              'history' \
              '</td>' \
              '</tr>')


    def printResult(self,job):
        if job.exception is not None:
            self._fileHandle.write('<!-- %s:%d %s-->' %(job.hostname, job.port, job.exception))
            return False

        self._fileHandle.write('<tr>')

        while True:
            #id
            self._fileHandle.write('<td>')
            self._fileHandle.write(str(self._index))
            self._fileHandle.write('</td>')
            self._index = self._index + 1

            #host
            self._fileHandle.write('<td>')
            url = 'http://%s:%d' % (job.hostname, job.port)
            self._fileHandle.write('<a href=%s>%s</a>' % (url, url))
            self._fileHandle.write('</td>')

            #title
            response_curr = job.result['response_get']
            self._fileHandle.write('<td>')
            try:
                body = HTTPBodyResponse(response_curr.content, response_curr.apparent_encoding)
                self._fileHandle.write(body.title)
                #pass
            except Exception as e:
                self._fileHandle.write(str(e))
            self._fileHandle.write('</td>')

            #information: server, cookies...
            response_curr = job.result['response_get']
            self._fileHandle.write('<td>')
            try:
                self._fileHandle.write('Status: %d<br/><br/>'%(response_curr.status_code))
                self.printFilterHeader(response_curr.headers)

                if len(response_curr.cookies):
                    self._fileHandle.write('<br/>Cookies:<br/>')
                    for name, value in response_curr.cookies.items():
                        self._fileHandle.write('%s : %s<br/>' % (name, value))

            except Exception as e:
                self._fileHandle.write(str(e))
            self._fileHandle.write('</td>')

            #option
            response_curr = job.result['response_options']
            self._fileHandle.write('<td>')
            try:
                self._fileHandle.write('Status: %d<br/><br/>'%(response_curr.status_code))
                self.printFilterHeader(response_curr.headers)
            except Exception as e:
                self._fileHandle.write(str(e))
            self._fileHandle.write('</td>')

            #history
            response_curr = job.result['response_get']
            self._fileHandle.write('<td>')
            try:
                for response in response_curr.history:
                    self._fileHandle.write('%s<br/>'%(response.status_code))
            except Exception as e:
                self._fileHandle.write(str(e))
            self._fileHandle.write('</td>')

            break

        self._fileHandle.write('</tr>')

        return False