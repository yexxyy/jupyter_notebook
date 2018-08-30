#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com>


import time
from concurrent.futures import as_completed,ProcessPoolExecutor,ThreadPoolExecutor

#耗cpu的操作，用多进程编程， 对于io操作来说， 使用多线程编程，进程切换代价要高于线程


def fib(n):
    """计算"""
    if n<=2:
        return 1
    return fib(n-1)+ fib(n-2)


def random_sleep(n):
    """io"""
    time.sleep(2)
    return n

def process_test(func):
    with ProcessPoolExecutor(3) as executor:
        all_task=[executor.submit(func,(num)) for num in [30]*10]
        start_time=time.time()
        for future in as_completed(all_task):
            data=future.result()
            # print('result:{}'.format(data))
        print('process time:{},func:{}'.format(time.time()-start_time,func.__name__))


def thread_test(func):
    with ThreadPoolExecutor(3) as executor:
        all_task=[executor.submit(func,(num)) for num in [30]*10]
        start_time=time.time()
        for future in as_completed(all_task):
            data=future.result()
            # print('result:{}'.format(data))
        print('thread time:{},func:{}'.format(time.time()-start_time,func.__name__))



#多进程
import os

def test_fork():
    a=1
    pid=os.fork()
    print('pid:',pid)
    if pid==0:
        a=a+1
    else:
        a=a+10
    print('a:',a)
    """
    pid: 32528
    a: 11
    pid: 0
    a: 2
    
    这里出现两次打印是因为，主线程一直往下运行，打印出0
    运行到os.fork()时，会将父进程的数据完整拷贝一份到子进程（进程间数据隔离）
    """
    
import multiprocessing

def get_html(n):
    time.sleep(n)
    print('get html end')
    return n

def multipricessiong_test():
    progress=multiprocessing.Process(target=get_html,args=(2,))
    progress.start()
    
    print(progress.pid)
    progress.join()
    print('main process end')


class ProcessiongTest(multiprocessing.Process):
    def run(self):
        pass

#进程池
def process_pool():
    pool=multiprocessing.Pool(multiprocessing.cpu_count())
    
    #apply_async() 返回 ApplyResult 类似线程的Future
    result=pool.apply_async(get_html,args=(3,))

    # pool停止接受新任务
    pool.close()
    
    #等待所有任务完成
    pool.join()
    
    print(result.get())


if __name__ == '__main__':
    
    
    # thread_test(fib)
    # process_test(fib)
    # thread_test(random_sleep)
    # process_test(random_sleep)
    
    """
    thread time:3.42461895942688,func:fib
    process time:1.5205891132354736,func:fib
    
    thread time:8.015908002853394,func:random_sleep
    process time:8.00415587425232,func:random_sleep
    """
    
    # test_fork()
    # multipricessiong_test()
    process_pool()