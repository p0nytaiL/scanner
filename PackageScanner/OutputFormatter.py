#!/usr/bin/python
#coding=utf-8


class OutputFormatter:
    def __init__(self):
        pass

    def printHeader(self, description):
        print '--------------- Result Header ---------------'

    def printFooter(self, description):
        print '\r--------------- Result Footer ---------------'

    def printResult(self, job):
        print job.id , 'done'


#为二阶扫描提供输入
class OutputFormatterNext(OutputFormatter):
    def __init__(self):
        OutputFormatter.__init__(self)

#输出到终端
class OutputFormatterConsole(OutputFormatter):
    def __init__(self):
        OutputFormatter.__init__(self)


#输出到文件
class OutputFormatterFile(OutputFormatter):
    def __init__(self):
        OutputFormatter.__init__(self)
        self._fileName = None
        self._fileHandle = None
        self._fileExt = '.txt'

    #打开文件文件
    #保存的文件名为description + 系统当前日期
    def printHeader(self, description):
        try:
            import time
            current_time = time.strftime('_%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
            self._fileName = description + current_time + self._fileExt
            self._fileHandle = open(self._fileName, 'w')
        except Exception as e:
            print __file__, e
            raise e

    #关闭文件
    def printFooter(self, description):
        #必须成功执行到printFooter才能释放fileHandle,有潜在的资源泄漏风险
        if self._fileHandle != None:
            print 'Scaner report: %s' % (self._fileName)
            self._fileHandle.close()

    #执行写入
    def printResult(self, job):
        pass

