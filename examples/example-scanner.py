#!/usr/bin/python
#coding=utf-8

from PackageScanner.JobQueue import Job
from PackageScanner.OutputFormatter import OutputFormatter
from PackageScanner.Scanner import Scanner_v1

'''
继承Job
    重写do方法
    返回值为do中通过网络请求获取到的结果
'''
class JobChar(Job):
    def __init__(self, id, char):
        Job.__init__(self, id)
        #以下部分自定义
        self._char = char

    def do(self):
        #想做什么可以自己实现
        #不要在do中实现print功能,do为多线程调用的方法,在此print,结果会乱成一团,
        #将需要打印的东西直接return
        #return后的参数会提交给OutputFormatter中的printResult方法
        if self._char == 't':
            self.is_last_job = True
        self.result = self._char
        return Job.do(self)


'''
继承OutputFormatter
    重写printResult

'''
class OutputFormatterChar(OutputFormatter):
    def __init__(self):
        OutputFormatter.__init__(self)

    #report_object参数为Job::do()方法的返回值
    #在printResult中统一进行打印
    def printResult(self, job):
        print '\r',job.result

'''
继承Scanner_v1
    重写createJobs
    用于生成Job对象
'''
class ScannerString(Scanner_v1):
    def __init__(self):
        Scanner_v1.__init__(self)
        self._description = '[print char]'#当前Scanner的描述
        self._outputFormatters.append(OutputFormatterChar())#此处关联上你自己实现的OutputFormatter


    def createJobs(self,targets):
        #此处创建你需要循环实现的Job
        for index, ch in enumerate(targets):
            self._jobQueue.addJob(JobChar(index+1, ch))

        return len(targets)#最好返回创建的Job个数,可以方便进度条的实现



if __name__ == '__main__':
    #创建一个Scanner
    #调用scan方法

    s = ScannerString()
    s.scan(targets='print each char in this string', thread_count= 1)

    #此处统一实现如此
    for r in s:
        pass

