#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import time
from datetime import datetime
import json
import traceback
from selenium import webdriver
from tasks.driver.amazon import AmazonDriver
from tasks.log.config import logger
from tasks.common import util


def register():
    logger.info("japan-register-user,start get ip ing... ")
    # fixme: this need to get the available ip add ip pool

    cur_ip = util.select_ip()
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

        worker.set_address({
            'username': username,
            'address': info[0],
            'state': info[1],
            'zip': info[2],
            'phone': phone,
        })

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
        logger.error(err)

    finally:
        driver.quit()
