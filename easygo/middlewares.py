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
from easygo.models import cookieObject
import time
import user_agents

from selenium import webdriver
from requests.exceptions import RequestException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver import ActionChains

from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware


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

    def process_request(self, request, spider):
        if len(spider.my_cookies.cookies) > 0:
            cookie = random.choice(spider.my_cookies.cookies)
            request.cookies = cookie
        else:
            print('Cookie已经用完')
        return None


class LocalRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response

        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        # customiz' here
        resp_dct = json.loads(response.body)
        if resp_dct.get('code') != 0:
            if (resp_dct.get('code') == -100) or (resp_dct.get('code') == -3):
                banned_cookie = request.cookies
                spider.my_cookies.remove_cookie(banned_cookie)
                spider.logger.info("Temporarily BANNED: %s." % banned_cookie)
                spider.logger.info("%s cookies left." % len(spider.cookies))
                # mongo_cli.cookies.find_one_and_update({"cookie": banned_cookie},
                #                                       {"$set": {"FailedDate": str(datetime.date.today())}})
            # spider.logger.warning("Url %s %s is rescheduled ." % (spider.all_urls[request.url],
            #                                                       request.url))
            return self._retry(request, response.body, spider) or response

        return response
