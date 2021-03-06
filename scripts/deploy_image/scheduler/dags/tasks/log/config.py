# -*- coding: utf-8 -*-

import logging.handlers
import logging

logger = logging.getLogger('airflow_app')  # 获取名为tst的logger

# LOG_FILE = '/scheduler/log/airflow_log.txt'
# file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
# fmt = '[%(asctime)s] [%(processName)s] [%(funcName)s] [%(levelno)s] %(name)-3s: %(levelname)-3s %(message).1000s'
# formatter = logging.Formatter(fmt)  # 实例化formatter
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)  # 为handler添加formatter
# logger.addHandler(file_handler)  # 为logger添加handler

console_handler = logging.StreamHandler()
cs_fmt = '[%(asctime)s] [%(processName)s] [%(funcName)s] [%(levelno)s] %(name)-3s: %(levelname)-3s: %(message).1000s'
console_handler.setFormatter(logging.Formatter(cs_fmt))
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)


