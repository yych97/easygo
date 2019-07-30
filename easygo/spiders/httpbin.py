# -*- coding: utf-8 -*-
import scrapy
from easygo import settings
import requests
import json
import yaml
import os

from scrapy.mail import MailSender
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

# mailers = MailSender(
#     smtphost="smtp.126.com",  # 发送邮件的服务器    
#     mailfrom="yych97@126.com",  # 邮件发送者
#     smtpuser="yych97@126.com",  # 用户名
#     smtppass="jkl8905201314",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
#     smtpport=25 # 端口号
# )  #初始化邮件模块

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    # def start_requests(self):
        # with open(settings.qq_list, 'r') as f: 
        #     test = yaml.load(f)
        #     print(test)
        #  self.acquire_cookies()

    def parse(self, response):
        print(json.loads(response.text)['origin'])
        # yield scrapy.Request(url=self.start_urls[0],dont_filter=True)
    
    def __init__(self):
        """ 监听信号量 """
        super(HttpbinSpider, self).__init__()# 当收到spider_closed信号的时候，调用下面的close方法来发送通知邮件
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider, reason):
        # 上方的信号量触发这个方法
        stats_info = self.crawler.stats._stats  # 爬虫结束时控制台信息
        body = "爬虫[%s]已经关闭，原因是: %s.\n以下为运行信息：\n %s" % (spider.name, reason, stats_info)
        subject = "[%s]爬虫关闭提醒" % spider.name
        mailers = MailSender(
            smtphost="smtp.126.com",  # 发送邮件的服务器    
            mailfrom="yych97@126.com",  # 邮件发送者
            smtpuser="yych97@126.com",  # 用户名
            smtppass="jkl8905201314",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
            smtpport=25  # 端口号
            # smtptls=True
        )  #初始化邮件模块
        mailers.send(to=["yych97@126.com"], subject=subject, body=body)
