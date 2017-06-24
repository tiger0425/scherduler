# -*- coding: utf-8 -*-
from os import environ

env = environ.get

USER_MYSQL_CONNSTR = env('USER_MYSQL_CONNSTR', '')
MAIL_OPTIONS = ['gmail.com', 'outlook.com', 'hotmail.com', 'outlook.jp', 'msn.com']
