#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com> 

import socket
import threading

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('0.0.0.0',8001))
server.listen()

def handle_sock(sock,addr):
    data = sock.recv(1024)
    print(addr,data.decode('utf8'))
    re_data = input()
    sock.send(re_data.encode('utf8'))
    

while True:
    sock,addr=server.accept()
    client_thread=threading.Thread(target=handle_sock,args=(sock,addr))
    client_thread.start()









