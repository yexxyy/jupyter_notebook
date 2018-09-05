#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com> 



import asyncio
import time

def callback(sleep_times):
    print('sleep {}'.format(sleep_times))
    

def stoploop(loop):
    loop.stop()

    
def call_soon_test():
    loop= asyncio.get_event_loop()
    loop.call_soon(callback,3)
    loop.call_later(1,callback,1)
    loop.call_later(2, callback, 2)
    loop.call_later(5,stoploop,loop)
    loop.call_soon_threadsafe(callback,4)
    loop.run_forever()
    
    
    
#ThreadPollExecutor和asycio完成阻塞IO请求


import socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def get_url(url):
    #通过socket请求html
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    #建立socket连接
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.setblocking(False)
    client.connect((host, 80)) #阻塞不会消耗cpu

    #不停的询问连接是否建立好， 需要while循环不停的去检查状态
    #做计算任务或者再次发起其他的连接请求

    client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))

    data = b""
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break

    data = data.decode("utf8")
    html_data = data.split("\r\n\r\n")[1]
    print(html_data)
    client.close()
    

def thread_poll_asyncio_test():
    """
    ThreadPollExecutor和asycio完成阻塞IO请求
    """
    start_time=time.time()
    loop=asyncio.get_event_loop()
    executor= ThreadPoolExecutor(3)
    tasks=[]
    for url in range(20):
        task=loop.run_in_executor(executor,get_url,'http://www.baidu.com')
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
    print('time:{}'.format(time.time()-start_time))
    

#asyncio模拟http请求
#aiohttp

async def get_url_with_async(url):
    #通过socket请求html
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    #建立socket连接
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.setblocking(False)
    reader,writer=await asyncio.open_connection(host, 80) #阻塞不会消耗cpu

    #不停的询问连接是否建立好， 需要while循环不停的去检查状态
    #做计算任务或者再次发起其他的连接请求
    
    
    # client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))
    writer.write("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))

    all_lines=[]
    async for row_line in reader:
        line=row_line.decode("utf8")
        all_lines.append(line)
    html='\n'.join(all_lines)
    return html

   


def asyncio_http_test():
    #版本一
    # start_time=time.time()
    # loop=asyncio.get_event_loop()
    # tasks=[]
    # for i in range(20):
    #     tasks.append(asyncio.ensure_future(get_url_with_async('http://www.baidu.com')))
    # loop.run_until_complete(asyncio.wait(tasks))
    # for task in tasks:
    #     print(task.result())
    # print(time.time()-start_time)
    
    #版本二

    start_time=time.time()
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio_http_test_main(loop))
    print(time.time()-start_time)


async def asyncio_http_test_main(loop):
    tasks=[]
    for i in range(20):
        tasks.append(asyncio.ensure_future(get_url_with_async('http://www.baidu.com')))
    for task in asyncio.as_completed(tasks):
        result = await task
        print(result)



#asyncio 同步和通信
from asyncio import Lock,Condition,Semaphore
total=0

async def add():
    global total
    for i in range(100000):
        total+=1
        
async def subtract():
    global total
    for i in range(100000):
        total-=1

def asyncio_sync():
    tasks=[add(),subtract()]
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(total)


async def get_stuff(url):
    # lock = Lock
    # await lock.acuqire()
    # #do something
    # lock.release()
    lock=Lock
    async with lock:
        pass
    
    

if __name__ == '__main__':
    # call_soon_test()
    # thread_poll_asyncio_test()
    # asyncio_http_test()
    # asyncio_http_test()
    
    asyncio_sync()