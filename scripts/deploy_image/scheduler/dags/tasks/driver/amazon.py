#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import threading
import random
import time
from urllib import quote
import urlparse
from urlparse import urljoin, parse_qs
from io import BytesIO
import traceback

from selenium.webdriver.common.keys import Keys  # 需要引入keys包
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
import requests
from selenium import webdriver
from pyquery import PyQuery

from tasks.log.config import logger
from tasks.common.useragent import UserAgent

user_agent = UserAgent()
cwd = os.getcwd()

# 导入时间戳替法


os.chdir(cwd)


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

    def is_element_exist(self, xpath, timeout=120):
        try:
            self.until(lambda d: self.driver.find_element_by_xpath(xpath), timeout)
            return True
        except Exception as e:
            logger.error(e.message)
            return False

    def go_home(self):
        self.go('https://{host}'.format(host=self.host))
        try:
            self.until(lambda d: self.driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]'), 60)
        except:
            raise Exception("网络发生异常")

    def until(self, method, timeout=115):
        wait = webdriver.support.ui.WebDriverWait(self.driver, timeout)
        return wait.until(method=method)

    def click(self, element):
        threading.Thread(target=lambda: element.click()).start()

    def submit(self, element):
        threading.Thread(target=lambda: element.click()).start()

    def login(self, email, password):
        print("current_url:" + self.driver.current_url)
        if not self.driver.current_url.startswith('https://{host}/ap/signin'.format(host=self.host)):
            print("go_home...host:" + self.host)
            self.go_home()
            try:
                self.click(self.until(lambda d: self.driver.find_element_by_id('nav-link-yourAccount')))
            except:
                self.click(self.until(lambda d: self.driver.find_element_by_id('nav-link-accountList')))
        self.until(lambda d: self.driver.find_element_by_id('signInSubmit'))
        self.driver.find_element_by_id('ap_email').send_keys(email)
        self.driver.find_element_by_id('ap_password').send_keys(password)
        self.submit(self.driver.find_element_by_id('signInSubmit'))

    def register(self, username, email, password):
        res = False
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

        self.submit(button)

        time.sleep(5)  # 缓迟五秒判断结果
        if 'https://{host}/ap/register'.format(host=self.host) in self.driver.current_url:  # 发生错误

            logger.error('quite the driver after the register')
            self.driver.quit()
            raise Exception('register have error')
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
        try:
            # self.driver.find_element_by_id('myab_newAddressButton').click()
            self.driver.find_element_by_xpath('//*[@id="a-autoid-0"]/span/input').click()
            time.sleep(5)

            s_url = self.driver.current_url
            if s_url.count('yaab-enterAddressSucceed', 0, len(s_url)) == 0:
                raise Exception('地址出错')
        except Exception as e:
            logger.error(e.message)
            raise Exception('添加地址不成功')

    def set_address_old(self, **kwargs):
        # 这里是同步的
        # self.go('https://{}/gp/css/account/address/view.html'.format(self.host))
        self.driver.get('https://{}/gp/css/account/address/view.html'.format(self.host))
        # self.driver.find_element_by_class_name('iux-main-content').find_element_by_class_name('amzn-btn').click()
        self.driver.find_element_by_xpath('//*[@id="iux-address-book"]/div[1]/a').click()
        self.driver.find_element_by_id('enterAddressFullName').send_keys(kwargs['username'])
        self.driver.find_element_by_id('enterAddressAddressLine1').send_keys(kwargs['address'])
        if self.host.endswith('co.jp'):
            webdriver.support.select.Select(
                self.driver.find_element_by_id('enterAddressStateOrRegion')
            ).select_by_value(kwargs['state'])
            zip_ = kwargs['zip'].split('-')
            self.driver.find_element_by_id('enterAddressPostalCode1').send_keys(zip_[0])
            self.driver.find_element_by_id('enterAddressPostalCode2').send_keys(zip_[1])
        else:
            self.driver.find_element_by_id('enterAddressCity').send_keys(kwargs['city'])
            self.driver.find_element_by_id('enterAddressStateOrRegion').send_keys(kwargs['state'])
            self.driver.find_element_by_id('enterAddressPostalCode').send_keys(kwargs['zip'])
        self.driver.find_element_by_id('enterAddressPhoneNumber').send_keys(kwargs['phone'])
        self.driver.find_element_by_id('myab_newAddressButton').click()
        try:
            self.driver.find_element_by_id('icam_addrSuggestionListSubmitButton').click()
        except:
            pass
        try:
            self.driver.find_element_by_id('myab_newAddressButton').click()
        except:
            pass

        try:
            self.driver.find_element_by_xpath('//*[@id="iux-address-book"]/div[1]/a')
        except:
            raise Exception('添加地址不成功')
            #
            # def add_to_cart_by_search(self, key, asin, shop_name, num=1, fba=False):
            #     ua = user_agent.random()
            #     session = requests.session()
            #     session.headers['User-Agent'] = ua
            #
            #     def _get_valid_search_page_url(url):
            #         url2 = urlparse(url)
            #         url = url2.scheme + '://' + url2.netloc + quote(url2.path) + \
            #               '?' + '&'.join([quote(k) + '=' + quote(v[0]) for k, v in parse_qs(url2.query).items()])
            #         resp = session.get(url, headers={'Referer': url})
            #         q = PyQuery(resp.content.decode('utf-8'))
            #         for li in q('[id^="result_"]').items():
            #             if li.attr['data-asin'] == asin:
            #                 return urljoin(self.driver.current_url, li('a').eq(0).attr.href)
            #         if not q('#pagnNextLink'):
            #             raise Exception('没找到asin')
            #         return _get_valid_search_page_url(urljoin(url, q('#pagnNextLink').eq(0).attr.href))
            #
            #     asin = asin.strip()
            #     url = _get_valid_search_page_url(
            #         'https://{host}/s/ref={key}?url=search-alias%3Daps&field-keywords={key}&page={page}'.format(
            #             host=self.host,
            #             key=key,
            #             page=1,
            #         ))
            #     self.add_to_cart_by_url(url, shop_name, num, fba=fba)
            #
            # def add_to_cart_by_url(self, key, asin, shop_name, num=1, fba=False):
            #     # 判断页面是否存在ASIN元素 存在则点击
            #     assert self.listpage_exists_product_element(key, asin,
            #                                                 lambda newurl: amazon_helper.update_shoppingcart_url(self.host,
            #                                                                                                      asin,
            #                                                                                                      newurl)), 'not find asin'
            #     self.click(
            #         self.until(
            #             lambda d: self.driver.find_element_by_xpath(
            #                 '//*[@data-asin="{}"]//a[contains(@class,"access-detail-page")]'.format(asin))))  # 点击浏览产品详情
            #     time.sleep(30)
            #     self.driver.switch_to_window(self.driver.window_handles[1])  # 定位到最后的标签页
            #
            #     try:
            #         if self.host == 'www.amazon.com':
            #             self.click(
            #                 self.until(
            #                     lambda d: self.driver.find_element_by_xpath('//*[@id="olp_feature_div"]/div/div[1]/span[1]/a'))
            #             )
            #         else:
            #             self.click(
            #                 self.until(lambda d: self.driver.find_element_by_xpath('//*[@id="olp_feature_div"]/div/span[1]/a')))
            #     except:
            #         try:
            #             if self.host == 'www.amazon.com':
            #                 self.click(
            #                     self.until(
            #                         lambda d: self.driver.find_element_by_xpath('//*[@id="mbc"]/div[3]/div/div/span[1]/a'))
            #                 )
            #             else:
            #                 self.click(
            #                     self.until(lambda d: self.driver.find_element_by_xpath('//*[@id="mbc"]/div[2]/div/span/a')))
            #         except:
            #             try:
            #                 self.click(self.driver.find_element_by_id('add-to-cart-button'))
            #             except:
            #                 self.click(self.driver.find_element_by_id('bb_atc_button'))
            #             return
            #
            #     for i in range(num):
            #         if i != 0:
            #             self.driver.back()
            #         ok = False
            #         divs = self.until(lambda d: self.driver.find_elements_by_class_name('olpOffer'))
            #
            #         if not ok:
            #             # 优先选择指定的发货方式
            #             for div in divs:
            #                 try:
            #                     self.until(lambda d: self.driver.find_element_by_css_selector('[class*="a-icon-prime"]'))
            #                     if not fba:
            #                         # 需要 自发货, 但是此时是fba, 所以跳过
            #                         continue
            #                 except:
            #                     if fba:
            #                         # 需要 fba, 但是此时不是fab, 所以跳过
            #                         continue
            #                 try:
            #                     a = div.find_element_by_class_name('olpSellerName').find_element_by_tag_name('a')
            #                     if a.get_attribute('innerText').strip() == shop_name.strip():
            #                         self.click(div.find_element_by_css_selector('[name="submit.addToCart"]'))
            #                         time.sleep(3)
            #                         ok = True
            #                         break
            #                 except:
            #                     pass
            #
            #         if not ok:
            #             # 尝试所有发货选项
            #             for div in divs:
            #                 try:
            #                     a = div.find_element_by_class_name('olpSellerName').find_element_by_tag_name('a')
            #                     if a.get_attribute('innerText').strip() == shop_name.strip():
            #                         self.click(div.find_element_by_css_selector('[name="submit.addToCart"]'))
            #                         time.sleep(3)
            #                         ok = True
            #                         break
            #                 except:
            #                     pass
            #
            #         if not ok:
            #             # 优先选择指定的发货方式 不限店铺
            #             for div in divs:
            #                 try:
            #                     self.until(lambda d: self.driver.find_element_by_css_selector('[class*="a-icon-prime"]'))
            #                     if not fba:
            #                         # 需要 自发货, 但是此时是fba, 所以跳过  driver.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
            #                         continue
            #                 except:
            #                     if fba:
            #                         # 需要 fba, 但是此时不是fab, 所以跳过
            #                         continue
            #                 try:
            #                     self.click(div.find_element_by_css_selector('[name="submit.addToCart"]'))
            #                     time.sleep(3)
            #                     ok = True
            #                     break
            #                 except:
            #                     pass
            #
            #         if not ok:
            #             # 随机选择 不限发货方式 不限店铺
            #             for div in divs:
            #                 try:
            #                     self.click(div.find_element_by_css_selector('[name="submit.addToCart"]'))
            #                     time.sleep(3)
            #                     ok = True
            #                     break
            #                 except:
            #                     pass
            #
            #         if not ok:
            #             raise Exception('没有找到asin对应的店铺')
            #
            # def checkout(self, credit_card=None, promo_code=None, email=None, password=None):
            #     self.go('/gp/cart/view.html/ref=nav_cart')
            #     self.submit(self.until(lambda d: self.driver.find_element_by_css_selector('[name="proceedToCheckout"]')))
            #     try:
            #         self.until(lambda d: self.driver.find_element_by_id('ap_email'), 25)
            #         assert email is not None and password is not None
            #         self.login(email, password)
            #     except Exception as e:
            #         print(e)
            #
            #     self.click(
            #         self.until(lambda d: self.driver.find_element_by_xpath('//*[@id="address-book-entry-0"]/div[2]/span')))
            #     self.submit(self.until(lambda d: self.driver.find_element_by_xpath(
            #         '//*[@id="shippingOptionFormId"]/div[3]/div/div/span[1]/span/input')))
            #     if promo_code and len(promo_code) > 3:
            #         self.click(self.until(lambda d: self.driver.find_element_by_id('gc-link-expander')))
            #         self.until(lambda d: self.driver.find_element_by_id('gcpromoinput')).send_keys(promo_code)
            #         self.submit(self.until(lambda d: self.driver.find_element_by_id('button-add-gcpromo')))
            #         time.sleep(3)
            #         try:
            #             if not self.until(lambda d: self.driver.find_element_by_id('pm_300'), timeout=5).is_selected():
            #                 self.click(self.until(lambda d: self.driver.find_element_by_id('pm_300'), timeout=5))
            #         except:
            #             pass
            #     elif credit_card and len(credit_card) > 3:
            #         if not self.until(lambda d: self.driver.find_element_by_id('ccAddCard')).is_displayed():
            #             self.driver.find_element_by_css_selector('[data-expander-anchor="new-cc-expander-anchor"]').click()
            #         self.until(lambda d: self.driver.find_element_by_id('ccName')).send_keys('Peter')
            #         self.until(lambda d: self.driver.find_element_by_id('addCreditCardNumber')).send_keys(credit_card)
            #         for i in range(10):
            #             try:
            #                 e = self.until(lambda d: self.driver.find_element_by_css_selector('[id*="_dropdown_combobox"]') \
            #                                .find_elements_by_tag_name('li')[8], 10)
            #                 if e.is_displayed():
            #                     e.click()
            #                     break
            #                 else:
            #                     self.until(lambda d: self.driver.find_element_by_xpath(
            #                         '//*[@id="form-add-credit-card"]/div[3]/div[4]/span[2]/span/span/button'), 10).click()
            #             except:
            #                 self.until(lambda d: self.driver.find_element_by_xpath(
            #                     '//*[@id="form-add-credit-card"]/div[3]/div[4]/span[2]/span/span/button'), 10).click()
            #
            #         try:
            #             self.driver.find_element_by_id('ccCVVNum').send_keys(str(random.randint(100, 999)))
            #         except:
            #             pass
            #         self.driver.find_element_by_id('ccAddCard').click()
            #         time.sleep(5)
            #
            #         try:
            #             self.until(lambda d: self.driver.find_element_by_css_selector('[id^="cardCurrency"]'),
            #                        timeout=5).click()
            #         except:
            #             pass
            #
            #     self.until(lambda d: self.driver.find_element_by_id('continue-top').is_displayed())
            #     self.submit(self.until(lambda d: self.driver.find_element_by_id('continue-top')))
            #
            #     try:
            #         self.until(
            #             lambda d: self.driver.find_element_by_xpath('//*[@id="address-book-entry-0"]/div[2]/span/a'),
            #             10,
            #         ).click()
            #     except:
            #         pass
            #
            #     try:
            #         self.until(lambda d: self.driver.find_element_by_id('prime-signup-button'), 10).click()
            #     except:
            #         pass
            #
            #     try:
            #         self.until(lambda d: self.driver.find_element_by_id('primeSignupButton'), 10).click()
            #     except:
            #         pass
            #
            #     try:
            #         self.until(
            #             lambda d: self.driver.find_element_by_xpath(
            #                 '//*[@id="primeAutomaticPopoverAdContent"]/div/div[1]/div[4]/span/span/input'),
            #             10,
            #         ).click()
            #     except:
            #         pass
            #
            #     try:
            #         self.until(
            #             lambda d: self.driver.find_element_by_css_selector('[name="action.checkoutAcceptOffer"]'),
            #             10,
            #         ).click()
            #     except:
            #         pass
            #
            #     if self.host == 'www.amazon.co.jp':
            #         try:
            #             self.until(lambda d: self.driver.find_element_by_id('marketplaceRadio'), timeout=5).click()
            #         except:
            #             pass
            #
            #     self.submit(self.until(lambda d: self.driver.find_element_by_css_selector('[name="placeYourOrder1"]')))
            #     try:
            #         return self.until(
            #             lambda d: self.driver.find_element_by_xpath('//*[@id="orders-list"]/div/span/b')).get_attribute(
            #             'innerText')
            #     except:
            #         return self.until(
            #             lambda d: self.driver.find_element_by_css_selector('[id*="order-number"]')).get_attribute("innerText")
            #
            # def shua_zan(self, email, password, url):
            #     self.login(email, password)
            #     self.go(url)
            #     self.until(lambda d: self.driver.find_element_by_class_name('votingButtonReviews')).click()
            #
            # def get_stock(self, url, shop_name):
            #     self.add_to_cart_by_url(url, shop_name, num=1, fba=True)
            #     self.go('/gp/cart/view.html/ref=nav_cart')
            #     self.click(self.until(lambda d: self.driver.find_element_by_id('a-autoid-2-announce')))
            #     self.click(self.until(lambda d: self.driver.find_element_by_class_name('quantity-option-10')))
            #     self.until(lambda d: self.driver.find_element_by_name('quantityBox')).send_keys('999')
            #     self.until(lambda d: self.driver.find_element_by_name('quantityBox')).send_keys(Keys.RETURN)
            #     time.sleep(10)
            #
            #     return int(self.driver.find_element_by_name('quantityBox').get_attribute('value'))
            #
            # def redeem_gifcard(self, gifcard):
            #     self.go('https://{}/gc/redeem/ref=gc_redeem_new_exp_DesktopRedirect'.format(self.host))
            #     e = self.until(lambda d: self.driver.find_element_by_id('gc-redemption-input'))
            #     e.send_keys(gifcard)
            #     # for c in gifcard:
            #     #     e.send_keys(c)
            #     self.submit(self.until(lambda d: self.driver.find_element_by_css_selector('[name="applytoaccount"]')))
            #     time.sleep(3)
            #
            #     # self.driver.find_element_by_id('gc-redemption-check-value-announce').click()
            #     # e = self.driver.find_element_by_id('gc-redemption-check-value-result')
            #     # if 'aok-hidden' in e.get_attribute('class'):
            #     #     self.driver.find_element_by_id('gc-redemption-apply-announce').click()
            #     # else:
            #     #     raise Exception('gifcard is not valid')
            #
            #
            # def listpage_exists_product_element(self, url, asin, method):
            #     newurl = None
            #     amazon_helper.replace(url)
            #     print(url)
            #     self.go(url)
            #
            #     def find_element():
            #         try:
            #             li_elements = self.until(lambda d: self.driver.find_elements_by_xpath(
            #                 '//*[@id="s-results-list-atf"]//li[contains(@class,"s-result-item")]'))
            #             assert len(li_elements) > 0
            #             self.driver.find_element_by_xpath('//*[@data-asin="{}"]'.format(asin))
            #             return True
            #         except:
            #             return False
            #
            #     def search_page():
            #         search_url = None
            #         # 向前搜索
            #         for i in range(1, 3):
            #             try:
            #                 pagn_element = self.until(lambda d: self.driver.find_element_by_xpath('//*[@id="pagn"]'))
            #                 element = pagn_element.find_element_by_xpath('//*[@id="pagnPrevLink"]')
            #                 self.driver.execute_script("arguments[0].click();", element)
            #                 # self.click(element)
            #                 if find_element():
            #                     search_url = self.driver.current_url
            #                     break
            #             except:
            #                 break;
            #         # 再次搜索本页
            #         if not search_url:
            #             # self.go(url)
            #             threading.Thread(target=lambda: self.driver.get(url)).start()
            #             if find_element():
            #                 search_url = self.driver.current_url
            #         # 向后搜索
            #         if not search_url:
            #             for i in range(1, 3):
            #                 try:
            #                     pagn_element = self.until(lambda d: self.driver.find_element_by_xpath('//*[@id="pagn"]'))
            #                     element = pagn_element.find_element_by_xpath('//*[@id="pagnNextLink"]')
            #                     self.driver.execute_script("arguments[0].click();", element)
            #                     if find_element():
            #                         search_url = self.driver.current_url
            #                         break
            #                 except:
            #                     break;
            #         # 返回URL
            #         return search_url
            #
            #     if find_element():
            #         newurl = url
            #     else:
            #         newurl = search_page()
            #
            #     if newurl != None and newurl != url:  # 执行更新回调函数
            #         print(newurl)
            #         method(newurl)
            #     if not newurl:
            #         return False
            #     else:
            #         return True
            #
            # def add_wishedlist_by_search(self, key, asin):
            #     if self.host == "www.amazon.co.jp":  #
            #         # 导航去个人中心创建心愿单文件夹
            #         time.sleep(25)
            #         self.click(
            #             self.until(lambda d: self.driver.find_element_by_xpath('//a[@id="nav-link-wishlist"]')))
            #
            #         if self.is_element_exist('//input[@name="submitForm"][@value="createNew"]'):
            #             self.click(
            #                 self.until(lambda d: self.driver.find_element_by_xpath(
            #                     '//input[@name="submitForm"][@value="createNew"]')))
            #
            #             try:  # 如果点击 右侧的设定超时 就从左侧选择 两者都超时，返回错误。
            #                 self.click(
            #                     self.until(lambda d: self.driver.find_element_by_xpath('//a[contains(text(),"リストの設定")]')))
            #             except:  # 备选方案
            #                 self.click(
            #                     self.until(lambda d: self.driver.find_element_by_xpath(
            #                         '//div[contains(@class,"a-fixed-right-grid wl-list selected")]//span[contains(text(),"非公开")]')))
            #
            #             if self.is_element_exist('//form[@id="g-manage-form"]//select') == False:  # 如果当前页面没有弹出窗体【网速缓慢情况】
            #                 self.go('https://{}/gp/registry/side/manage/ref=cm_wl_privacy_settings_nojs'.format(self.host))
            #                 assert self.is_element_exist(
            #                     '//form[@id="g-manage-form"]//select'), 'not find g-manage-form select '
            #
            #             Select(self.until(
            #                 lambda d: self.driver.find_element_by_xpath(
            #                     '//form[@id="g-manage-form"]//select'))).select_by_value('0')
            #             self.click(
            #                 self.until(
            #                     lambda d: self.driver.find_element_by_xpath(
            #                         '//form[@id="g-manage-form"]//input[@type="submit"]')))
            #
            #         # 导航去列表页面寻找ASIN码
            #         assert self.listpage_exists_product_element(key, asin,
            #                                                     lambda newurl: amazon_helper.update_wisedlist_url(self.host,
            #                                                                                                       asin,
            #                                                                                                       newurl)), 'not find asin'
            #         self.click(
            #             self.until(
            #                 lambda d: self.driver.find_element_by_xpath(
            #                     '//*[@data-asin="{}"]//a[contains(@class,"access-detail-page")]'.format(asin))))
            #
            #         # 切换最后一个Tab 点击右侧添加至心愿单
            #         time.sleep(30)
            #         self.driver.switch_to_window(self.driver.window_handles[1])  # 定位到最后一页
            #         self.click(
            #             self.until(
            #                 lambda d: self.driver.find_element_by_xpath(
            #                     '//*[@id="add-to-wishlist-button-submit"]')))
            #         time.sleep(5)
            #     else:
            #
            #         # 判断页面是否存在ASIN元素 存在则点击
            #         assert self.listpage_exists_product_element(key, asin,
            #                                                     lambda newurl: amazon_helper.update_wisedlist_url(self.host,
            #                                                                                                       asin,
            #                                                                                                       newurl)), 'not find asin'
            #         self.click(
            #             self.until(
            #                 lambda d: self.driver.find_element_by_xpath(
            #                     '//*[@data-asin="{}"]//a[contains(@class,"access-detail-page")]'.format(asin))))  # 点击浏览产品详情
            #         self.click(
            #             self.until(
            #                 lambda d: self.driver.find_element_by_xpath(
            #                     '//*[@id="add-to-wishlist-button-submit"]')))  # 点击产品页左侧的添加心愿单
            #         time.sleep(10)  # 延迟10秒判断当前页面
            #         if self.driver.current_url.count('/gp/product/handle-buy-box/ref=dp_start-bbf_1_glance', 0,
            #                                          len(self.driver.current_url)) == 0:
            #             self.click(
            #                 self.until(
            #                     lambda d: self.driver.find_element_by_xpath('//*[@id="WLNEW_newwl_section"]/a')))  # 设置为公开的心愿单
            #             self.click(
            #                 self.until(
            #                     lambda d: self.driver.find_element_by_id('WLNEW_submit')))  # 点击添加到心愿单 /html/body/div[4]/input
            #
            #         else:
            #             self.click(
            #                 self.until(
            #                     lambda d: self.driver.find_element_by_xpath('//input[@type="image"]')))  # 设置为公开的心愿单
            #         time.sleep(5)  # 延迟5秒  quit
            #
            # def add_wishedlist_by_search_old(self, key, asin):
            #     ua = user_agent.random()
            #     session = requests.session()
            #     session.headers['User-Agent'] = ua
            #
            #     def _get_valid_search_page_url(url):
            #         url2 = urlparse(url)
            #         url = url2.scheme + '://' + url2.netloc + quote(url2.path) + \
            #               '?' + '&'.join([quote(k) + '=' + quote(v[0]) for k, v in parse_qs(url2.query).items()])
            #         resp = session.get(url, headers={'Referer': url})
            #         q = PyQuery(resp.text)
            #         for li in q('[id^="result_"]').items():
            #             if li.attr['data-asin'] == asin:
            #                 return urljoin(self.driver.current_url, li('a').eq(0).attr.href)
            #         if not q('#pagnNextLink'):
            #             raise Exception('没找到asin')
            #         return _get_valid_search_page_url(urljoin(url, q('#pagnNextLink').eq(0).attr.href))
            #
            #     asin = asin.strip()
            #     url = _get_valid_search_page_url(
            #         'https://{host}/s/ref={key}?url=search-alias%3Daps&field-keywords={key}&page={page}'.format(
            #             host=self.host,
            #             key=key,
            #             page=1,
            #         ))
            #     self.add_wishedlist_by_url(url)
            #
            # def add_wishedlist_by_url(self, url):
            #     self.go(url)
            #     self.click(self.until(lambda d: self.driver.find_element_by_id('add-to-wishlist-button-submit')))
            #     try:
            #         self.click(
            #             self.until(
            #                 lambda d: self.driver.find_element_by_xpath('//*[@id="WLNEW_newwl_submit"]/div/div[1]/span[1]')))
            #     except:
            #         pass
            #     try:
            #         self.until(lambda d: self.driver.find_element_by_id('WLNEW_submit')).click()
            #     except:
            #         pass
            #     try:
            #
            #         self.until(
            #             lambda d: self.driver.find_element_by_css_selector("input[type='image']")).click()
            #     except:
            #         pass
            #     time.sleep(5)
            #
            # # PC端浏览任务
            # def add_browse_by_pc(self, asin):
            #     asin = asin.strip()
            #     # step 1 .导航到首页
            #     # 输入关键词
            #     self.until(lambda d: self.driver.find_element_by_id('twotabsearchtextbox')).send_keys(asin)
            #     # 点击搜索 提交
            #     self.click(
            #         self.until(
            #             lambda d: self.driver.find_element_by_xpath('//input[@type="submit"][@class="nav-input"]')))
            #
            #     # step 2 .进入到列表页面
            #     assert self.is_element_exist('//*[@data-asin="{}"]'.format(asin)), '找不到ASIN码'
            #
            #     self.until(
            #         lambda d: self.driver.find_element_by_xpath(
            #             '//a[contains(@href,"{}")][contains(@class,"access-detail-page")]'.format(asin))).click()
            #
            #     # step 3. 随机浏览
            #     max_scroll_count = random.randint(20, 35)
            #     scroll_index = 0;
            #     while scroll_index < max_scroll_count:
            #         if scroll_index < 5:
            #             scroll_height = random.randint(500, 1000)
            #         else:
            #             up_or_down = random.randint(1, 2)
            #             if up_or_down == 1:
            #                 scroll_height = random.randint(500, 1000)
            #             else:
            #                 scroll_height = random.randint(-1000, -500)
            #         scroll_sleep = random.randint(1, 5)
            #         self.driver.execute_script("window.scrollBy(0,{})".format(scroll_height))
            #         time.sleep(scroll_sleep)
            #         scroll_index += 1
