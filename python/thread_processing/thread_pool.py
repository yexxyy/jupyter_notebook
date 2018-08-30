#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com> 

#线程池 进程池编程包
"""
控制数量
任务状态／返回值
当一个线程完成，主线程立马知晓
多线程／多进程编程接口一致
"""
from concurrent.futures import ThreadPoolExecutor,as_completed,wait,ALL_COMPLETED,FIRST_COMPLETED
import time

def get_html(times):
    time.sleep(times)
    print('get page {}'.format(times))
    return times
    
    




#ThreadPoolExecutor 使用方法一
def test():
    executor = ThreadPoolExecutor(max_workers=2)
    task1 = executor.submit(get_html, (3))
    task2 = executor.submit(get_html, (2))
    
    print('cancel:', task1.cancel())
    
    time.sleep(2)

    # task.done()判断任务是否完成，立即返回
    print(task1.done(), task2.done())

    # task.result() 获取任务返回结构，阻塞
    print(task1.result())


#ThreadPoolExecutor 使用方法二
def future():
    executor = ThreadPoolExecutor(max_workers=2)
    urls=[3,2,1,5]
    all_task=[executor.submit(get_html,(url)) for url in urls]
    
    wait(all_task,return_when=FIRST_COMPLETED)
    
    for future in as_completed(all_task):
        data=future.result()
        print('result {}'.format(data))


#ThreadPoolExecutor 使用方法三
def future3():
    executor = ThreadPoolExecutor(max_workers=2)

    for data in executor.map(get_html,[2,3,4,5]):
        print('result {}'.format(data))
    
    
    

if __name__ == '__main__':
    #test()
    
    future()
    #future3()





