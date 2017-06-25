#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium import webdriver
from tasks.log.config import logger
from tasks.common.useragent import UserAgent

user_agent = UserAgent()


class AmazonDriver(object):
    def __init__(self, driver=None, host='www.amazon.com', captcha='127.0.0.1:8000'):
        self.driver = driver
        self.host = host
        self.captcha = captcha
        self.driver.implicitly_wait(1)
        self.driver.set_window_size(1920, 1080)
        self.driver.set_page_load_timeout(120)

    def go(self, url):
        self.driver.get(url)

    def go_home(self):
        self.go('https://{host}'.format(host=self.host))
        self.until(lambda d: self.driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]'), 60)

    def _find_element_by_id(self, element_id=None):
        ele = ''
        try:
            ele = self.driver.find_element_by_id(element_id)
        except Exception as e:
            logger.error(e.message)
            logger.error('not find the element by the id of {}'.format(element_id))
        return ele

    def until(self, method, timeout=115):
        wait = webdriver.support.ui.WebDriverWait(self.driver, timeout)
        return wait.until(method=method)

    def click(self, element):
        element.click()

    def login(self, email, password):
        logger.info("current_url:" + self.driver.current_url)
        if not self.driver.current_url.startswith('https://{host}/ap/signin'.format(host=self.host)):
            logger.info("go_home...host:" + self.host)
            self.go_home()
            try:
                self.click(self.until(lambda d: self.driver.find_element_by_id('nav-link-yourAccount')))
            except:
                self.click(self.until(lambda d: self.driver.find_element_by_id('nav-link-accountList')))
        self.until(lambda d: self.driver.find_element_by_id('signInSubmit'))
        self.driver.find_element_by_id('ap_email').send_keys(email)
        self.driver.find_element_by_id('ap_password').send_keys(password)
        self.driver.find_element_by_id('signInSubmit').click()

    def register(self, username, email, password):

        logger.info('start to get the main page')
        self.go_home()
        logger.info('finish render the home page and do next task')
        e = self.until(lambda d: self.driver.find_element_by_id('nav-flyout-ya-newCust'))

        a = e.find_element_by_tag_name('a')
        self.go(a.get_attribute('href'))

        button = self.until(lambda d: self.driver.find_element_by_id('continue'))
        self.driver.find_element_by_id('ap_customer_name').send_keys(username)

        if self.host.endswith('co.jp'):
            self.driver.find_element_by_id('ap_customer_name_pronunciation').send_keys(username)

        if self.host.endswith('.in'):
            self.driver.find_element_by_id('ap_use_email').click()

        self.driver.find_element_by_id('ap_email').send_keys(email)
        self.driver.find_element_by_id('ap_password').send_keys(password)

        if not self.host.endswith('.in'):
            self.driver.find_element_by_id('ap_password_check').send_keys(password)

        # find the continue button
        logger.info('find the continue button and do click')
        button.click()

        time.sleep(5)  # 缓迟五秒判断结果
        if 'https://{host}/ap/register'.format(host=self.host) in self.driver.current_url:  # 发生错误

            logger.error('quite the driver after the register')
            self.driver.quit()
            logger.error('register have error')
            return False

        logger.info('finish register the user: {} - {} - {}'.format(username, email, password))
        return True

    def set_address(self, user_info):
        self.driver.get('https://{}/a/addresses/add?ref_=ya_add_address_yaab'.format(self.host))

        self.driver.find_element_by_id('address-ui-widgets-enterAddressFullName').send_keys(user_info['username'])
        self.driver.find_element_by_id('address-ui-widgets-enterAddressLine1').send_keys(user_info['address'])

        if self.host.endswith('co.jp'):
            webdriver.support.select.Select(
                self.driver.find_element_by_id('address-ui-widgets-enterAddressStateOrRegion-dropdown-nativeId')
            ).select_by_value(user_info['state'])
            zip_ = user_info['zip'].split('-')
            self.driver.find_element_by_id('address-ui-widgets-enterAddressPostalCodeOne').send_keys(zip_[0])
            self.driver.find_element_by_id('address-ui-widgets-enterAddressPostalCodeTwo').send_keys(zip_[1])
        else:
            self.driver.find_element_by_id('address-ui-widgets-enterAddressCity').send_keys(user_info['city'])
            self.driver.find_element_by_id('address-ui-widgets-enterAddressStateOrRegion').send_keys(user_info['state'])
            self.driver.find_element_by_id('address-ui-widgets-enterAddressPostalCode').send_keys(user_info['zip'])
        self.driver.find_element_by_id('address-ui-widgets-enterAddressPhoneNumber').send_keys(user_info['phone'])

        self.driver.find_element_by_xpath('//*[@id="a-autoid-0"]/span/input').click()
        time.sleep(5)

        s_url = self.driver.current_url
        # ???? what's this
        if s_url.count('yaab-enterAddressSucceed', 0, len(s_url)) == 0:
            logger.error('the address error ')
        else:
            logger.info('now set address success!')
