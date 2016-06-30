#!/opt/local/bin/python
#coding=utf-8


import email.header
import email.message
import email.parser
import email.utils

from PackageScanner.JobQueue import Job

class JobEMLParser(Job):
    def __init__(self, id, eml_file):
        Job.__init__(self, id)
        self.eml_file = eml_file
        self.eml_msg = None


    '''
    fp, email.header
    '''
    def do(self):

        try:
            fp = open(self.eml_file, 'r')

            parser = email.parser.HeaderParser()

            self.eml_msg = parser.parse(fp)

        except Exception as e:
            pass

        return Job.do(self)

from PackageScanner.OutputFormatter import OutputFormatterConsole
class OutputFormatterEmailContacts(OutputFormatterConsole):
    def __init__(self):
        OutputFormatterConsole.__init__(self)
        self.results = {}

    def printResult(self, job):
        for k, v in job.eml_msg.items():
            if k.lower() in ('from'):
                real_name, address = email.utils.parseaddr(v)
                name, corp = address.split('@')
                if self.results.get(corp) == None:
                    self.results[corp] = set()

                real_name, chartset = email.header.decode_header(real_name)[0]
                if chartset != None:
                    real_name = real_name.decode(chartset)
                if len(real_name) != 0:
                    name = '%s (%s)' % (name, real_name)
                self.results[corp].add(name)



from PackageScanner.Scanner import Scanner_v1
import os
class ScannerEmailContacts(Scanner_v1):
    def __init__(self):
        Scanner_v1.__init__(self)
        self._outputFormatters.append(OutputFormatterEmailContacts())
        self._enable_header = False
        self._enable_footer = False

    '''
    提交路径,抽取路径中的eml文件进行解析
    '''
    def createJobs(self, targets):
        path_root = targets
        #path_root = '/Users/ponytail/Desktop/Shared/install'
        total = 1
        for dirpath, dirnames, eml_files in os.walk(path_root):
            for file_index, eml_file in enumerate(eml_files):
                eml_file = os.path.join(dirpath, eml_file)
                if os.path.isfile(eml_file):
                    self._jobQueue.addJob(JobEMLParser(file_index + total, eml_file))

        return total


if __name__ == '__main__':

    path_root = '/maibox'
    s = ScannerEmailContacts()
    s._description = 'eml parser test'
    s.scan(targets= path_root, thread_count= 1)
    for r in s:
        pass

    for k, v in s._outputFormatters[0].results.items():
        print k
        for name in v:
            print '\t' , name
        print ''