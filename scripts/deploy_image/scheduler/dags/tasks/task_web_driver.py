# -*- coding: utf-8 -*-
from config import logger
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tasks.common.decorator import timeout


@timeout(20)
def get_cnblogs(*arg, **kwargs):
    logger.info('start the session')
    # chioce = random.choice([0,1])
    # headers = DesiredCapabilities.CHROME
    # if chioce:
    headers = DesiredCapabilities.FIREFOX

    driver = webdriver.Remote(command_executor='http://10.10.2.38:4444/wd/hub',
                              desired_capabilities=headers)
    logger.info('get the webdriver')
    try:
        logger.info('begin get the url')
        driver.get('http://brucedone.com')

        source = driver.page_source
        if isinstance(source, str):
            source = source.decode('utf-8')
        logger.info('get the result')
        return 'get the source'
    except Exception as e:
        logger.error(e.message)
    finally:
        driver.close()
