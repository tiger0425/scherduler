# -*- coding: utf-8 -*-

import logging.handlers
import logging

logger = logging.getLogger('airflow')  # 获取名为tst的logger

LOG_FILE = 'airflow_log.txt'
file_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
fmt = '%(asctime)s, [%(processName)s], %(name)-3s, %(levelname)s, %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)  # 为handler添加formatter
logger.addHandler(file_handler)  # 为logger添加handler

console_handler = logging.StreamHandler()
cs_fmt = '%(asctime)s, [%(processName)s], %(name)-3s, %(levelname)s, %(message)s'
console_handler.setFormatter(logging.Formatter(cs_fmt))
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)
logger.info('first info message')
logger.info('first info message')
logger.info('first info message')
logger.debug('first debug message')
