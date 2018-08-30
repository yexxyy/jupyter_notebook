#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com> 

import dis

def add(a,):
    a=a+1
    return a
    
#多线程修改同一个数据造成数据紊乱解释：程序执行的最小单元是 字节码片段
# dis.dis(add)
"""
8           0 LOAD_FAST                0 (a)
            2 LOAD_CONST               1 (1)
            4 BINARY_ADD
            6 STORE_FAST               0 (a)

9           8 LOAD_FAST                0 (a)
            10 RETURN_VALUE
"""

#同步方式一
from threading import Lock,RLock

def sync_one():
    lock = Lock()
    lock.acquire()
    # do something chagge data
    lock.release()

    # RLock 在同一个线程里可以连续调用多次lock.acquire, 务必与release次数相等



#同步方式二 condition 用于线程间复杂通信
from  threading import Condition,Thread

class TianMao(Thread):
    
    def __init__(self,cond):
        super(TianMao, self).__init__(name='天猫')
        self.cond=cond
    
    def run(self):
        with self.cond:
            print('{}:Hello'.format(self.name))
            self.cond.notify()
            self.cond.wait()

            print('{}:I am fine,and you?'.format(self.name))
            self.cond.notify()
            self.cond.wait()

class XiaoAi(Thread):
    def __init__(self, cond):
        super(XiaoAi, self).__init__(name='小爱')
        self.cond = cond
    
    def run(self):
        with self.cond:
            
            self.cond.wait()
            print('{}:How do you do?'.format(self.name))
            self.cond.notify()

            self.cond.wait()
            print('{}:Yes,I am fine,too.'.format(self.name))
            self.cond.notify()
            
            
def condition_test():
    cond=Condition()
    thread1=TianMao(cond)
    thread2=XiaoAi(cond)

    #线程的启动顺序：最先wait的线程要先启动
    thread2.start()
    thread1.start()
    

#同步方式三 Semaphore :用于控制进入数量的锁
#写只允许一个线程，读取则可以允许多个线程
import time
from threading import Semaphore

class HtmlSpider(Thread):
    def __init__(self,url,sem):
        super(HtmlSpider, self).__init__()
        self.url=url
        self.sem=sem
    
    def run(self):
        time.sleep(2)
        print('load {} success'.format(self.url))
        self.sem.release()


class UrlProducer(Thread):
    def __init__(self,sem):
        super(UrlProducer, self).__init__()
        self.sem=sem
    
    def run(self):
        for i in range(20):
            self.sem.acquire()
            html_thread=HtmlSpider('https://baidu.com/{}/'.format(i),self.sem)
            html_thread.start()




if __name__ == '__main__':
    # condition_test()
    
    sem=Semaphore(3)
    url_producer=UrlProducer(sem)
    url_producer.start()