from config import logger
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_cnblogs(*arg,**kwargs):
    driver = webdriver.Remote(command_executor='http://hub:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME)

    try:
        driver.get('https://www.cnblogs.com')
        source = driver.page_source
        return source
    except Exception as e:
        logger.error(e.message)
    finally:
        driver.close()


