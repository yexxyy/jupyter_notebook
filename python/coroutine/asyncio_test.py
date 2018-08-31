#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<me@xander-ye.com> 



import asyncio

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
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    call_soon_test()
