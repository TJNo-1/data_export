#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import time
from alert_script import send_message

def get_mem():
    # 内存使用率
    # 交换分区使用率

    ret = subprocess.Popen('free -m',shell=True,stdout=subprocess.PIPE)
    free_m = ret.stdout.readlines()
    phy_message = free_m[1]
    phy_result = re.match(r'Mem:\s*(\d+)\s*(\d+)',phy_message)
    phy_usage = float(phy_result.group(2))/float(phy_result.group(1))

    swap_messgae = free_m[2]
    swap_result = re.match(r'Swap:\s*(\d+)\s*(\d+)',swap_messgae)
    swap_usage = float(swap_result.group(2))/float(swap_result.group(1))

    return "%.2f" % phy_usage ,"%.2f" % swap_usage
def get_cup():
    ret = subprocess.Popen('top -b -n 1| grep Cpu',shell=True,stdout=subprocess.PIPE)
    cpu_message = ret.stdout.readlines()[0]
    cpu_info_lst = cpu_message.split(',')

    _result_lst = []
    for i in range(5):
        get_mess = re.match(r'.*\s+(\d+\W\d+).*',cpu_info_lst[i])
        _result_lst.append(get_mess.group(1))

    return _result_lst

    # ['%Cpu(s): 15.8 us,  2.9 sy,  0.0 ni, 80.9 id,  0.1 wa,  0.0 hi,  0.2 si,  0.0 st\n']
    # us: 用户进程占用 CPU 百分比
    # sy: 内核进程占用 CPU 百分比
    # id: CPU 空闲百分比
    # wa: IO 等待百分比

if __name__ == '__main__':
    while True:
        phy_usage, swap_usage = get_mem()
        cpu_list = get_cup()
        cpu_list.append(phy_usage)
        cpu_list.append(swap_usage)
        cpu_list.pop(2)
        cpu_list.pop(2)
        mess_list = ['CPU-用户进程使用率','CPU-内核进程使用率','CPU-IO率','物理内存使用率','交换分区使用率']

        # ['14.0', '2.8', '0.8', '0.33', '0.00']
        # 用户进程使用率, 内核进程使用率,IO率, 物理内存使用率,交换分区使用率

        for _index in range(len(cpu_list)):
            if float(cpu_list[_index]) > 75.0:
                _str = '**WARNING**\n'+mess_list[_index]+':'+cpu_list[_index]+'%\n'+'数据拷贝工作已停止运行'
                send_message(_str)
                break


        # send_info = '物理内存使用率:{}%\n交换分区使用率:{}%\nCPU-用户进程使用率:{}%\nCPU-内核进程使用率:{}%\n' \
        #             'CPU-空闲率:{}%\nCPU-IO率:{}%\n'.format(phy_usage,swap_usage,cpu_list[0],cpu_list[1],
        #                                               cpu_list[3],cpu_list[4])
        # send_message(send_info)
        time.sleep(30)




