#!/usr/bin/python
#coding=utf-8

import sys

from PackageScanner.JobQueue import JobQueue_v1
from PackageScanner.OutputFormatter import OutputFormatter


class Scanner_v1:
    def __init__(self):
        self._jobQueue = JobQueue_v1()
        self._description = ''
        self._outputFormatters = []
        self._enable_header = True
        self._enable_footer = True

    def createJobs(self,targets):
        pass

    def scan(self, targets, thread_count):
        if 0 == len(self._outputFormatters):
            self._outputFormatters.append(OutputFormatter())

        try:
            self._jobQueue.start(thread_count)

            if len(self._description) == 0:
                self._description = str(targets)

            print 'Scan Job %s with %d threads started !' % (self._description, thread_count)
            count = self.createJobs(targets)

            for outputFormatter in self._outputFormatters:
                if self._enable_header:
                    outputFormatter.printHeader(self._description)

            self._jobQueue._eventAllJobAdded.set()

        except Exception as e:
            self._jobQueue._eventAllJobAdded.set()
            self.stop()
            print __file__, e
            exit(-1)

    def __iter__(self):
        return self

    #终止任务的判定由Scanner完成
    def next(self):
        try:
            finished_job = self._jobQueue.next()#raise StopIneration

            #终止任务判定
            if finished_job.is_last_job:
                raise StopIteration

        except StopIteration as stop:
            self.stop()
            print '\rScanner Result Summary:'
            print '\t','unfinished %d jobs' % (self._jobQueue._queueUnfinishedJobs.qsize())
            print '\t','timeout %d jobs' % (self._jobQueue._queueTimeoutJobs.qsize())
            raise StopIteration

        #print '\r',' '*30,
        #返回可用于下阶段扫描的结果
        r = None
        for outputFormatter in self._outputFormatters:
                r = outputFormatter.printResult(finished_job)

        print '\r', str(self._jobQueue._progress.progress()), '%',#finished_job.description,
        sys.stdout.flush()
        return r


    def stop(self):
        self._jobQueue.stop()
        for outputFormatter in self._outputFormatters:
            if self._enable_footer:
                r = outputFormatter.printFooter(self._description)



if __name__ == '__main__':
    print 'see example : examples/example-scanner.py'