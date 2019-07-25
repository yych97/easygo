# -*- coding: utf-8 -*-
import scrapy
from easygo import settings
import requests
import json
import yaml
import os


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def start_requests(self):
        with open(settings.qq_list, 'r') as f: 
            test = yaml.load(f)
            print(test)
        #  self.acquire_cookies()

    def parse(self, response):
        print(json.loads(response.text)['origin'])
        yield scrapy.Request(url=self.start_urls[0],dont_filter=True)
