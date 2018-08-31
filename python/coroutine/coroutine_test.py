#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com> 


#生成器进阶 send、 close、 throw 、yeild from
#协程 async、 await

async def downloader(url):
    return url

async def download_url(url):
    html=await downloader(url)
    return html

"""
事件循环+回调（驱动生成器）+epoll（io多路复用）
asyncio是python用于解决异步io编程的一整套解决方案

torando、 gevent、twisted(scrapy,django channels)
torando(实现了web服务器,可以搭配nginx直接部署)，django/flask(uwsgi,gunicorn+nginx)

"""

import asyncio
import time

#将函数包装成另一个函数
from functools import partial

async def get_html(url):
    print('start get url')
    await asyncio.sleep(2)
    print('get utl end')
    return 'xander'
    
    

def callback(url,future):
    print('complished: {}'.format(url))
    
    
def asyncio_test1():
    """单个任务"""
    start_time = time.time()
    loop = asyncio.get_event_loop()
    task = loop.create_task(get_html('http://www.baidu.com'))
    task.add_done_callback(partial(callback, 'http://www.baidu.com'))
    loop.run_until_complete(task)
    print(task.result())
    print(time.time() - start_time)
    

def asyncio_test2():
    """多个任务"""
    start_time = time.time()
    loop = asyncio.get_event_loop()

    tasks = [get_html('http://www.baidu.com') for i in range(10)]
    get_future = asyncio.ensure_future(asyncio.gather(*tasks))
    loop.run_until_complete(get_future)
    print(get_future.result())
    print(time.time() - start_time)
  
def asyncio_test3():
    """
    gather比wait 更加high-level
    """
    loop = asyncio.get_event_loop()
    tasks1 = [get_html('http://www.baidu.com') for i in range(10)]
    tasks2 = [get_html('http://www.baidu.com') for i in range(10)]
    tasks1=asyncio.gather(*tasks1)
    tasks2=asyncio.gather(*tasks2)
    
    # tasks1.cancel()
    
    loop.run_until_complete(asyncio.gather(tasks1,tasks2))
    

async def get_html_test(sleep_times):
    print('waiting')
    await asyncio.sleep(sleep_times)
    print('done {}'.format(sleep_times))

def asyncio_test4():
    """
    task取消
    """
    task1=get_html_test(2)
    task2 = get_html_test(10)
    task3 = get_html_test(1)
    tasks= [task1,task2,task3]
    loop=asyncio.get_event_loop()
    
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt as e:
    
        all_tasks=asyncio.Task.all_tasks()
        for task in all_tasks:
            print(task.cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()
    
    
    
async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))
    
def asyncio_test5():
    """
    协程嵌套协程
    https://docs.python.org/3/library/asyncio-task.html
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_sum(1, 2))
    loop.close()
    

if __name__ == '__main__':
    
    # asyncio_test1()
    # asyncio_test2()
    # asyncio_test3()
    # asyncio_test4()
    asyncio_test5()
    
    