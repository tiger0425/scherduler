#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json
import traceback
from tasks.driver.amazon import AmazonDriver
from tasks.log.config import logger
from tasks.common import util
from tasks.ip import manage
from tasks.settings import PROXY_USER, PROXY_PASSWORD


def refresh_4g_and_ready_ip():
    tag = 'default'
    ip = manage.get_ip(tag)
    logger.info('get the ip:{} from proxy server'.format(ip))

    host = ip.split(':')[0]
    if not manage.ping(host):
        raise ValueError('error,current ip is not reachable ,please use another one :{}'.format(ip))

    # login and refresh
    if not manage.dialup_4g(host, PROXY_USER, PROXY_PASSWORD):
        raise ValueError('error,failed to re-dial 4g ,please check it :{}'.format(ip))

    return ip


def register(cur_ip):
    logger.info("japan-register-user,start get ip ing... ")
    # fixme: this need to get the available ip add ip pool

    # cur_ip = refresh_4g_and_ready_ip()
    logger.info('get the ip of {}'.format(cur_ip))
    if not cur_ip:
        logger.info('get none ip return ,end the task')
        return

    driver = util.make_driver(cur_ip)
    try:

        username = util.select_user_name()
        email, password = util.make_user()
        worker = AmazonDriver(driver, host='www.amazon.co.jp', captcha='127.0.0.1:6000')
        res = worker.register(username, email, password)

        info = util.select_user_info()
        phone = util.make_phone()

        # worker.set_address({
        #     'username': username,
        #     'address': info[0],
        #     'state': info[1],
        #     'zip': info[2],
        #     'phone': phone,
        # })

        # output the result
        user = {
            'username': username,
            'address': info[0],
            'state': info[1],
            'zip': info[2],
            'phone': phone,
            'nickname': username,
            'email': email,
            'password': password,
        }

        if res:
            logger.info('register success:' + json.dumps(user))

    except Exception as e:
        err = traceback.format_exc()
        logger.error(e.message)
        logger.error(err)

    finally:
        driver.quit()
