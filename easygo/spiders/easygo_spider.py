# -*- coding: utf-8 -*-
import scrapy
from easygo import settings
import requests
import json
import time
import sys
import pandas
import os
import datetime

import transCoordinateSystem
from easygo.items import EasygoItem

# #创建一个异常类，用于在cookie失效时抛出异常
# class CookieException(Exception):
#     def __init__(self):
#         Exception.__init__(self)

class EasygoSpiderSpider(scrapy.Spider):
    name = 'easygo_spider'
    allowed_domains = ['c.easygo.qq.com']
    center = []
    qq_number_sides = settings.qq_number_sides
    time_now_str = ''
    # cookies = []

    def start_requests(self):
        url = 'http://c.easygo.qq.com/api/egc/heatmapdata'
        self.center = self.return_center()
        # self.acquire_cookies()
        self.time_now_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        spyder_list = self.spyder_list_all()
        for item in spyder_list:
            """这部分负责每个qq号码抓取的次数"""
            params = self.spyder_params(item)
            request = scrapy.Request(url=url+'?'+params, method='GET', callback=self.parse_data, dont_filter=True)
            yield request

    def parse_data(self, response):
        text = response.body_as_unicode()
        node_list = json.loads(text)["data"]
        code = json.loads(text)["code"]
        uin = response.request.cookies['uin']
        # print(response.request.headers['User-Agent'])
        if (node_list != "") and (code == 0):
            print(uin + ' OK')
            try:
                min_count = node_list[0]["count"]
                for i in node_list:
                    min_count = min(i['count'],min_count)
                for i in node_list:
                    count = i['count']/min_count
                    gcj_lng = 1e-6 * (250.0 * i['grid_x'] + 125.0) #此处的算法在宜出行网页后台的js可以找到，文件路径是http://c.easygo.qq.com/eg_toc/js/map-55f0ea7694.bundle.js
                    gcj_lat = 1e-6 * (250.0 * i['grid_y'] + 125.0)
                    lng, lat = transCoordinateSystem.gcj02_to_wgs84(gcj_lng, gcj_lat)
                    item = EasygoItem(lng=lng, lat=lat, count=count, time=self.time_now_str)
                    yield item
            except IndexError as e:
                pass
        else:
            print(uin + ' No Data')
            print(text)

    # 自定义函数
    def spyder_params(self, item):
        """将传入的块转化为网页所需的表单"""
        lng_min,lng_max,lat_min,lat_max = item
        lng_min,lat_min = transCoordinateSystem.wgs84_to_gcj02(lng_min,lat_min)
        lng_max,lat_max = transCoordinateSystem.wgs84_to_gcj02(lng_max,lat_max)
        lng = (lng_min+lng_max)*0.5
        lat = (lat_min+lat_max)*0.5
        params = "lng_min="+str(lng_min)+"&lat_max="+str(lat_max)+"&lng_max="+str(lng_max)+"&lat_min="+str(lat_min)+"&level=16"+"&city=%E6%88%90%E9%83%BD"+"&lat=undefined"+"&lng=undefined"+"&_token="
        return params

    def spyder_list_all(self):
        """获取所需爬取的所有块"""
        spyder_list_all = []
        for item in self.center:
            lng,lat = item
            lng,lat = float(lng),float(lat)
            spyder_list_all.append([lng-0.5*settings.lng_delta,lng+0.5*settings.lng_delta,lat-0.5*settings.lat_delta,lat+0.5*settings.lat_delta])
        return spyder_list_all
    
    def return_center(self):
        xy_data = settings.xy_name
        center_list = []
        with open (xy_data,'r',encoding='utf-8') as f:
            for item in f.readlines()[1:]:
                center_list.append(tuple(item.strip().split(",")[-2:]))
        return center_list

    # def acquire_cookies(self):
    #     cookie_filename = settings.cookie_file
    #     if not os.path.exists(cookie_filename):
    #         with open (cookie_filename,'w',encoding='utf-8') as f:
    #             for number in self.qq_number_sides:
    #                 cookie = self.get_cookie(number)
    #                 f.write(json.dumps(cookie))
    #                 f.write('\n')
    #                 self.cookies.append(cookie)
    #     else:
    #         cookies_fromfile = []
    #         with open (cookie_filename,'r',encoding='utf-8') as f:
    #             cookies_fromfile = f.readlines()
    #         for cookie_str in cookies_fromfile:
    #             cookie_str = cookie_str.strip('\n')
    #             self.cookies.append(json.loads(cookie_str)) 
                
