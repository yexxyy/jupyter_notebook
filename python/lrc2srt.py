#!/usr/bin/env playground
# -*- coding: utf-8 -*-
# lrc2srt.py in jupyter_notebook
# Created by yetongxue at 2024/3/12
# lrc歌词转srt字幕
import re
import datetime


def main():
    f = open("/Users/yetongxue/Downloads/布列瑟农.lrc", 'r')
    content = f.readlines()

    time_cache = {}
    for index, line in enumerate(content):
        time, current_lrc = line.split(']')
        time = time[1:]
        minute, second_tmp = time.split(':')
        second, microsecond = second_tmp.split('.')
        if not microsecond:
            microsecond = 0
        #     print(minute, int(float(second) * 60/100), microsecond)
        #     if int(minute) >= 1:
        #         second=int(float(second) * 60/100)
        #     else:
        second = int(second)
        time = datetime.datetime(year=2023, month=11, day=23, hour=0, minute=int(minute), second=second, microsecond=int(int(microsecond) * 10000))
        time_str = time.strftime('%H:%M:%S,%f')
        timestr = time_str[:-3]
        time_cache[timestr] = current_lrc
    time_cache['00:04:15,000'] = ''

    lasttime = None
    lastlrc = None
    count = -1
    rows = []
    for k, v in time_cache.items():
        if lasttime:
            row = f'{count}\n{lasttime} --> {k}\n{lastlrc}'
            rows.append(row)
        lasttime = k
        lastlrc = v
        count += 1
    wf = open('/Users/yetongxue/Downloads/布列瑟农.srt', 'w')
    wf.write('\n'.join(rows))
    wf.close()


if __name__ == '__main__':
    main()
