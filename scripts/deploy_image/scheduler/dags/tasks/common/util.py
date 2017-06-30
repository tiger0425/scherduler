# -*- coding: utf-8 -*-
import random
import hashlib
import os
from selenium import webdriver
from tasks.common.useragent import UserAgent
from tasks.common.data import USER_INFO, USER_NAME, IP_POOL
from tasks.settings import MAIL_OPTIONS


def make_user():
    account = hashlib.md5(os.urandom(8)).hexdigest()[:16] + '@' + random.choice(MAIL_OPTIONS)
    password = hashlib.md5(os.urandom(8)).hexdigest()[:16]
    return account, password


def make_driver(ip):
    options = webdriver.ChromeOptions()
    # 2017-04-14 设置代理
    # host = ip + ':8888'
    host = '192.168.201.195:8888'
    options.add_argument('browserName=chrome')
    options.add_argument('--proxy-server=http://' + host)

    ua = UserAgent()
    user_agent = ua.random()
    options.add_argument('--user-agent=' + user_agent)

    # 无图模式
    options.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2})
    driver = webdriver.Remote('http://192.168.1.251:4444/wd/hub', options.to_capabilities())
    return driver


def make_phone():
    phone = '0' + random.choice('123456789') + str(random.random())[2:11]
    return phone


def select_ip():
    return random.choice(IP_POOL)


# fixme: need add data middle ware ,data should store in database
def select_user_name(country=None):
    return random.choice(USER_NAME)


def select_user_info(country=None):
    return random.choice(USER_INFO).split('@')
