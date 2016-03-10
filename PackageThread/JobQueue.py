#!/usr/bin/python
#coding=utf-8
__author__ = 'ponytail'


import Queue
import threading

'''
BugFix
    加入retry job的主线程与JobQueue中的工作线程存在时差
    没有遵守原子性

    工作线程判定工作队列为空,正常退出
    主线程存在往JobQueue中添加任务的可能

    此时已无工作线程,结果队列也不可能再有结果输入.判定JobQueue解释的条件成立
    Scanner达成退出逻辑
    导致扫描完毕之后,还有没有执行的Job(超时的Job)

    调整Job超时判定到JobQueue中,使JobQueue在逻辑上满足原子性
    is_last_job的判定也移动到JobQueue中
    Scanner对Job执行判定,手工结束Job
'''

class Progress:
    def __init__(self):
        self._index = 0
        self._total = 0

    def progress(self):
        return '%.2f' % ((float(self._index)/ float(self._total)) *100)

    def __str__(self):
        return self.progress()

'''
https://pymotw.com/2/Queue/

重构后的JobQueue包含三个队列
_queueWorkingJobs
    执行中的Job队列

_queueFinishedJobs
    Job执行完毕之后的结果
    存入该队列,直接从该队列获取Job对象

_queueUnfinishedJobs
    手工Stop之后,_wokringQueue中的Job转移到该队列中,后续考虑进行序列化处理,可以重新导入未完成的任务

_queueWorkingThreads
    需要有维护一个存放了当前线程对象的变量,不然无法控制,访问线程的状态

'''
class JobQueue_v1:
    def __init__(self):
        self._queueWorkingJobs = Queue.Queue()#Queue.LifoQueue()
        self._queueFinishedJobs = Queue.Queue()
        self._queueUnfinishedJobs = Queue.Queue()
        self._queueWorkingThreads = Queue.Queue()
        self._eventAllJobAdded = threading.Event()
        self._queueTimeoutJobs = Queue.Queue()
        self._progress = Progress()

    def start(self, num_of_threads):
        for i in range(0, num_of_threads):
            t = threading.Thread(target=self.doJob)
            t.start()
            self._queueWorkingThreads.put(t)

    '''
        停止操作不引入新的事件对象,而是将_workingQueue中的Job转移到_unfinishedQueue
        workingThread判定_wokingQueue是否为空来中断线程的操作
        尚不明确是否存在线程安全问题
    '''
    def stop(self):
        self._queueUnfinishedJobs = self._queueWorkingJobs
        self._queueWorkingJobs = Queue.Queue()
        self._queueWorkingThreads.join()
        #print 'all working threads exited'

    #超时重试的判定,由Scanner移入JobQueue
    def doJob(self):
        while True:
            if self._eventAllJobAdded.is_set() and self._queueWorkingJobs.empty(): break

            try:
                job = self._queueWorkingJobs.get(timeout=2)#上一时刻非空,此时并不一定非空,不加timeout可能挂起
                finished_job = job.do()#job中的异常最好由job自己处理

                #超时重试
                if finished_job.is_timeout and (finished_job.retry < finished_job.max_retry):
                    #print "检测到超时任务", finished_job.hostname
                    finished_job.retry = finished_job.retry + 1
                    finished_job.is_timeout = False
                    self._queueWorkingJobs.put(finished_job)
                    continue

                if finished_job.is_timeout and (finished_job.retry == finished_job.max_retry):
                    #print "无效任务"
                    self._queueTimeoutJobs.put(finished_job)
                    #continue

                #无超时,加入结果队列
                self._progress._index = self._progress._index + 1
                self._queueFinishedJobs.put(finished_job)

            except Queue.Empty as e:
                continue

        self._queueWorkingThreads.get()
        self._queueWorkingThreads.task_done()

    def addJob(self,job):
        self._queueWorkingJobs.put(job)
        self._progress._total = self._progress._total + 1

    def next(self):
        finished_job = None
        while True:
            try:
                finished_job = self._queueFinishedJobs.get(timeout=2)
                break
            except Queue.Empty as e:
                if self._queueWorkingThreads.empty() and self._queueFinishedJobs.empty():
                        raise StopIteration
                continue

        return finished_job

    def __iter__(self):
	    return self

'''
负责完整的业务处理
扫描结果的打印统一由Job返回result后,提交给OutputFormatter处理

    每个job都有一个id,可以同于调试
    self.id

    #重试次数
    self.retry

    #判定当前job执行是否超时
    self.is_timeout

    #job执行结果统一保存
    self.result

    #对于爆破类型的扫描,该标示用于终止扫描
    self.is_last_job

为了便于框架调用获取完整的job信息,do方法中的返回值为self
所有继承job的实现,都必须在do方法中返回self
'''
class Job:
    def __init__(self,id):
        self.id = id
        self.retry = 1
        self.max_retry = 3
        self.is_timeout = False
        self.result = None
        self.is_last_job = False
        self.exception = None

    #job中的异常最好由job自己处理
    #派生类必须在重写的do中return该方法
    def do(self):
        return self

#example
if __name__ == '__main__':
    jobQueue = JobQueue_v1()
    jobQueue.start(4)
    for i in range(200,300):
        jobQueue.addJob(Job(i))

    jobQueue._eventAllJobAdded.set()

    for index,result in enumerate(jobQueue):
        print index,result