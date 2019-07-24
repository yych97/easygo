# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests
import json
import os
from easygo import settings
from easygo.models import proxyObject
import time
import user_agents

from selenium import webdriver
from requests.exceptions import RequestException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver import ActionChains


class EasygoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class EasygoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgentDownloaderMiddleware(object):

    def process_request(self, request, spider):
        user_agent = random.choice(user_agents.agents)
        request.headers['User-Agent'] = user_agent
        return None


class ProxyDownloaderMiddleware(object):
    times = 0
    proxy = ''

    def process_request(self, request, spider):
        if self.times % 8 == 0:
            proxyO = proxyObject()
            self.proxy = proxyO.get_proxy_txt()
        self.times = self.times + 1
        # print(self.times)
        request.meta['proxy'] = self.proxy
        return None


class CookieDownloaderMiddleware(object):
    cookies = []
    times = 0
    cookie_num = settings.cookie_numbers
    cookie_fre_list = []
    i = -1
    AUTO_SET_FRE = settings.AUTO_SET_FRE
    fre = settings.fre
    qq_number_sides = settings.qq_number_sides

    def __init__(self):
        self.acquire_cookies()
        if self.AUTO_SET_FRE == False:
            for num in self.cookie_num:
                uin = self.cookies[num]['uin']
                fre = int(input('请输入Cookie({})的fre：'.format(uin)))
                self.cookie_fre_list.append(fre)

    def process_request(self, request, spider):
        # if len(self.cookies) == 0:
        #     self.acquire_cookies()
        if self.times % self.fre == 0:
            self.i = self.i + 1
            if self.AUTO_SET_FRE == False:
                if self.i < len(self.cookie_num):
                    self.fre = self.cookie_fre_list[self.i]
                self.times = 0
        if self.i < len(self.cookie_num):
            request.cookies = self.cookies[self.cookie_num[self.i]]
        else:
            print('Cookie已经用完')
        self.times = self.times + 1
        return None
    
    def acquire_cookies(self):
        cookie_filename = settings.cookie_file
        if not os.path.exists(cookie_filename):
            with open (cookie_filename,'w',encoding='utf-8') as f:
                for number in self.qq_number_sides:
                    cookie = self.get_cookie(number)
                    f.write(json.dumps(cookie))
                    f.write('\n')
                    self.cookies.append(cookie)
        else:
            cookies_fromfile = []
            with open (cookie_filename,'r',encoding='utf-8') as f:
                cookies_fromfile = f.readlines()
            for cookie_str in cookies_fromfile:
                cookie_str = cookie_str.strip('\n')
                self.cookies.append(json.loads(cookie_str))

    def get_cookie(self, qq_number_side):
        """负责跟据传入的qq号位次，获得对应的cookie并返回，以便用于爬虫"""
        while True:
            try:
                chromeOptions = webdriver.ChromeOptions()
                proxyO = proxyObject()
                chrome_proxy = proxyO.get_proxy_txt()
                # self.proxy.append(chrome_proxy)
                chromeOptions.add_argument('--proxy-server=http://{}'.format(chrome_proxy))
                chromedriver = r'./chromedriver'
                os.environ["webdriver.chrme.driver"] = chromedriver
                chrome_login = webdriver.Chrome(chromedriver)
                chrome_login.get("https://ui.ptlogin2.qq.com/cgi-bin/login?pt_hide_ad=1&style=9&appid=549000929&pt_no_auth=1&pt_wxtest=1&daid=5&s_url=https%3A%2F%2Fh5.qzone.qq.com%2Fmqzone%2Findex")
                while True:
                    try:
                        num = qq_number_side
                        qq_num = settings.qq_list[num][0]
                        qq_passwd = settings.qq_list[num][1]
                        print (qq_num)
                        break
                    except IndexError as e:
                        pass
                        # globals()["qq_number_sides"] = 0
                time.sleep(1)
                chrome_login.find_element_by_id("u").send_keys(qq_num)
                chrome_login.find_element_by_id("p").send_keys(qq_passwd)
                # chrome_login.maximize_window()
                chrome_login.find_element_by_id("go").click()
                time.sleep(3)
                
                # 当遇到qq号不能登录时，手动输入其他qq号
                if ("安全验证" in chrome_login.page_source) and (chrome_login.current_url=="https://ui.ptlogin2.qq.com/cgi-bin/login?pt_hide_ad=1&style=9&appid=549000929&pt_no_auth=1&pt_wxtest=1&daid=5&s_url=https%3A%2F%2Fh5.qzone.qq.com%2Fmqzone%2Findex"):
                    time.sleep(5)
                if ("你输入的帐号或密码不正确，请重新输入。"or"为了账号安全，请使用一键登录。" in chrome_login.page_source) and (chrome_login.current_url=="https://ui.ptlogin2.qq.com/cgi-bin/login?pt_hide_ad=1&style=9&appid=549000929&pt_no_auth=1&pt_wxtest=1&daid=5&s_url=https%3A%2F%2Fh5.qzone.qq.com%2Fmqzone%2Findex"):
                    chrome_login.quit()
                    qq_number_side = int(input('登录错误，请输入其他QQ号再次尝试：'))
                    continue
                
                time.sleep(5)                        
                cookie_items = chrome_login.get_cookies()
                chrome_login.quit()
                user_cookie = {}
                for cookie_item in cookie_items:
                    user_cookie[cookie_item["name"]] = cookie_item["value"]
                # globals()["qq_number_sides"] += 1
                print(user_cookie)
                return user_cookie
            except WebDriverException as e:
                try:
                    chrome_login.close()
                    print(e)
                except Exception:
                    pass
