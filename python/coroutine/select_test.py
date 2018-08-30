#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com> 

from selectors import DefaultSelector,EVENT_READ,EVENT_WRITE
from urllib.parse import urlparse
import socket

selector=DefaultSelector()
urls=['http://www.baidu.com']
stop=False

class Fetcher():
    
    def connected(self,key):
        
        #取消监听
        selector.unregister(key.fd)
        
        self.client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(
                self.path,self.host
        ).encode('utf8'))
        selector.register(self.client.fileno(),EVENT_READ,self.readable)
        
        
    def readable(self,key):
        d = self.client.recv(1024)
        if d:
            self.data += d
        else:
            # 数据读完之后取消监听
            selector.unregister(key.fd)
            data = self.data.decode('utf8')
            html_data = data.split('\r\n\r\n')[1]
            print(html_data)
            self.client.close()
            urls.remove(self.current_url)
            if not urls:
                global stop
                stop=True
        
    
    def get_url(self,url):
        self.current_url=url
        url=urlparse(url)
        self.host=url.netloc
        self.path=url.path
        self.data=b''
        if self.path=='':
            self.path='/'
            
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.setblocking(False)
        
        try:
            self.client.connect((self.host,80))
        except BlockingIOError as e:
            pass
        
        
         
        
        #监听socket是否连接好
        #注册文件描述符self.client.fileno()，事件EVENT_WRITE,回调函数
        selector.register(self.client.fileno(),EVENT_WRITE,self.connected)





def loop():
    #事件循环，不停的请求socket的状态，并调用对应的回调函数
    while not stop:
        ready=selector.select()
        for key,mask in ready:
            
            #把回调函数拿出来
            call_back=key.data
            call_back(key)


if __name__ == '__main__':
    
    for url in urls:
        fetcher=Fetcher()
        fetcher.get_url(url)
        loop()