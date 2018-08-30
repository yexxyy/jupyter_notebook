#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com> 

# from queue import Queue

from multiprocessing import Queue,Pool,Manager,Pipe,Process

#进程间通信 方式一
#通过Pipe在进程间通信,pipe只能适用于两个进程,其性能比Queue高
def producer(pipe):
    pipe.send('xander')

def consumer(pipe):
    print(pipe.recv())



def pipe_test():
    
    receive_pipe,send_pipe=Pipe()
    my_producer=Process(target=producer,args=(send_pipe,))
    my_consumer=Process(target=consumer,args=(receive_pipe,))
    
    my_consumer.start()
    my_producer.start()
    my_consumer.join()
    my_producer.join()
    
    

#进程间通信 方式二

def add_data(p_dict,key,value):
    p_dict[key]=value


def manager_test():
    progress_dict=Manager().dict()
    
    first_progress=Process(target=add_data,args=(progress_dict,'xander',3))
    second_progress=Process(target=add_data,args=(progress_dict,'xander2',5))

    first_progress.start()
    second_progress.start()
    first_progress.join()
    second_progress.join()
    
    print(progress_dict)

    
if __name__ == '__main__':
    # pipe_test()

    manager_test()