#!/usr/bin/python
#coding=utf-8


from PackageScanner.OutputFormatter import *

class OutputFormatterConsoleHTTPServer(OutputFormatterConsole):
    def __init__(self):
        pass

    def printHeader(self, description):
        print '--------------------------------------------------------------------------------------------------------------------------'
        print '%15s     %85s       '%('IP', 'Title')
        print '--------------------------------------------------------------------------------------------------------------------------'

    #Print Title
    def printResult(self, result):
        if result.exception != None:
            #print '\r%s:%d\t'%(result.hostname, result.port), result.exception
            return None
        try:
            print '\r%s:%d\t%85s'%(result.hostname, result.port, result.result['response_body']['title'])
        except:
            print result.hostname, result.port

    def printFooter(self, description):
        print '\r--------------------------------------------------------------------------------------------------------------------------'
        print '%15s     %85s'%('IP', 'Title')
        print '--------------------------------------------------------------------------------------------------------------------------'


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
            'cache-control'
        ]
        for header_name, header_value in headers.items():
            if header_name in filter:   continue
            self._fileHandle.write(header_name + ': ' + header_value +'<br/>')

    def printHeader(self, description):
        self._fileName = description + '.html'
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
        if job.result['error_body'] is not None:
            self._fileHandle.write(str(job.result['error_body']))
        else:
            self._fileHandle.write('%s' % (job.result['response_body']['title']))
        self._fileHandle.write('</td>')

        #head
        self._fileHandle.write('<td>')
        if job.result['error_head'] is not None:
            self._fileHandle.write(str(job.result['error_head']))
        else:
            self._fileHandle.write('status %s<br/>' % (job.result['response_head']['status']))
            self.printFilterHeader(job.result['response_head']['headers'])
        self._fileHandle.write('</td>')

        #option
        self._fileHandle.write('<td>')
        if job.result['error_options'] is not None:
            self._fileHandle.write(str(job.result['error_options']))
        else:
            self._fileHandle.write('status %s<br/>' % (job.result['response_options']['status']))
            self.printFilterHeader(job.result['response_options']['headers'])
        self._fileHandle.write('</td>')

        #robots
        self._fileHandle.write('<td>')
        if job.result['error_robots'] is not None:
            self._fileHandle.write(str(job.result['error_robots']))
        else:
            self._fileHandle.write(job.result['response_robots']['body'].replace('\n','<br/>'))
        self._fileHandle.write('</td>')
        self._fileHandle.write('</tr>')

        return False

    def printFooter(self, description):
        if self._fileHandle != None:
            self._fileHandle.write('</table></html>')
        OutputFormatterFile.printFooter(self, description)

