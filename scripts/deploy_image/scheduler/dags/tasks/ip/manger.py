# -*- coding:utf-8 -*-
import paramiko
import os
import time
from tasks.log.config import logger


def dialup_4g(host, user, psw):
    # 拔号
    flag = False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=psw, timeout=300)
    stdin, stdout, stderr = ssh.exec_command('rc4g rc4g')

    logger.info('拨号成功。。等待十秒判断灯。。。')
    time.sleep(10)
    stdin, stdout, stderr = ssh.exec_command(
        "ubus call network.interface.4g status  | grep address | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'")
    strout = str(stdout.read())

    logger.info('灯返回。。。{0}'.format(strout))
    if len(strout) > 0:
        flag = True
    ssh.close()
    return flag


# PING  IP  如果成功返回True，失败返回False
def ping(ip_addr):
    for i in range(1, 3):
        ret = os.system("ping -c 1 -W 1 %s" % ip_addr)
        if ret == 0:  # PING成功
            return True
    else:
        return False


def get_ip(u_lock=''):
    # 队列获取IP
    get_thread_lock.acquire()  # 锁住资源
    ip_addr = ip_manage.get(u_lock)
    get_thread_lock.release()  # 释放资源
    if ip_addr != None:
        ping_statu = ping(ip_addr)
        if ping_statu:
            if dialup_4g(ip_addr, 'root', 'admin') == False:
                ip_manage.failed(ip_addr)
                time.sleep(2)  # 延迟2秒 再去获取IP
                ip_addr = get_ip(u_lock)
            else:
                ip_manage.successed(ip_addr)
        else:
            ip_manage.failed(ip_addr)
            time.sleep(2)  # 延迟2秒 再去获取IP
            ip_addr = get_ip(u_lock)
    else:
        time.sleep(2)  # 延迟2秒 再去获取IP
        ip_addr = get_ip(u_lock)

    return ip_addr


def put_ip(ip_addr):
    ip_manage.put(ip_addr)
