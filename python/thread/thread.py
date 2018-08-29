#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com>


import time
import threading

def get_detail_html(url):
    print('detail start')
    time.sleep(4)
    print('detail end')
    
    
def get_detail_url(url):
    print('detail url start')
    time.sleep(2)
    print('detail url end')
    
    
   
def thread():
    """多线程 方法一"""
    therad1 = threading.Thread(target=get_detail_html, args=('',))
    thread2 = threading.Thread(target=get_detail_url, args=('',))
    
    # 设置Daemon为True时，主线程退出，子线程也将被kill
    therad1.setDaemon(True)
    # thread2.setDaemon(True)
    start_time = time.time()
    therad1.start()
    thread2.start()

    # join()将会等到所有线程执行完成之后才会往下执行
    thread2.join()
    therad1.join()
    print('last_time:{}'.format(time.time() - start_time))


class GetDetailHtml(threading.Thread):
    def run(self):
       while True:
           time.sleep(2)
           print(self._args.get())


class GetDetailUrl(threading.Thread):
    def run(self):
        for i in range(10):
            self._args.put(i)
            time.sleep(1)
        

def thread2():
    """多线程 方法二"""
    thread1=GetDetailHtml(name='get_detail_html')
    thread2=GetDetailUrl(name='get_detail_url')

    start_time = time.time()
    thread1.start()
    thread2.start()

    # join()将会等到所有线程执行完成之后才会往下执行
    thread2.join()
    thread1.join()
    print('last_time:{}'.format(time.time() - start_time))


#线程间的通信
#方式一 ：新建一个文件variable.py，将所有需要用到的变量放在里面统一管理
# 使用时这样导入 from thread.variables import varizble_params,修改变量时加锁

#方式二：queue
from queue import Queue

def queue_test():
    params=Queue(maxsize=1000)

    thread1 = GetDetailHtml(name='get_detail_html',args=params)
    thread2 = GetDetailUrl(name='get_detail_url',args=params)

    start_time = time.time()
    thread1.start()
    thread2.start()

    # join()将会等到所有线程执行完成之后才会往下执行
    thread2.join()
    thread1.join()




if __name__ == '__main__':
    
    #方法一
    #thread()
    
    #方法二
    # thread2()
    
    #线程间通信：queue
    queue_test()