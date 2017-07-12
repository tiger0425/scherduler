# -*- coding: utf-8 -*-
from os import environ

env = environ.get

USER_MYSQL_CONNSTR = env('USER_MYSQL_CONNSTR', '')
MAIL_OPTIONS = ['gmail.com', 'outlook.com', 'hotmail.com', 'outlook.jp', 'msn.com']

IP_PROXY_SERVER = env('PROXY_SERVER', 'http://192.168.1.251:9000')
SELENIUM_HUB_SERVER = env('SELENIUM_HUB_SERVER', 'http://192.168.1.251:4444/wd/hub')

PROXY_USER = env('PROXY_USER', 'root')
PROXY_PASSWORD = env('PROXY_USER', 'admin')

FUNC_TIMEOUT = int(env('FUNC_TIMEOUT', 60 * 10))
DIAL_TIME_OUT = int(env('DIAL_TIME_OUT', 16))
