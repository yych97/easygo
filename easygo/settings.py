# -*- coding: utf-8 -*-

# Scrapy settings for easygo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'easygo'

SPIDER_MODULES = ['easygo.spiders']
NEWSPIDER_MODULE = 'easygo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'easygo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
  'Referer': 'http://c.easygo.qq.com/eg_toc/map.html?origin=csfw'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'easygo.middlewares.CookieSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'easygo.middlewares.UserAgentDownloaderMiddleware': 543,
   # 'easygo.middlewares.ProxyDownloaderMiddleware': 542,
   'easygo.middlewares.CookieDownloaderMiddleware': 541,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'easygo.pipelines.EasygoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_FILE = 'tecent25m.log'
LOG_LEVEL = 'INFO'
LOG_ENABLED = False
CONCURRENT_ITEMS = 500

# ******************************************* #

# Custom Settings for easygo project

#生成cookie使用到的QQ号
qq_number_sides = [7, 8]
#本次爬取使用的cookie行号
cookie_numbers = [0, 1]
#所有的QQ号列表
qq_list = [
]

xy_name = "sh_noCM.txt"
cookie_file = "qq_cookie.txt"

#代理池
proxy_url = "http://api.ip.data5u.com/dynamic/get.html?order=3ad7917c16dc90af3b87941f5e9c173b&ttl=1&sep=3"
# proxy_url = "http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=1&ys=1&cs=1&lb=4&sb=0&pb=45&mr=1&regions=&gm=4"
# proxy_url = "http://api.ip.data5u.com/dynamic/get.html?order=3ad7917c16dc90af3b87941f5e9c173b&ttl=1&random=true&sep=3"

#下面设置文件存目录，不要设置在系统盘，不然会出现问题
#当前目录用"."表示，如"./example/"
filepath = r"./data/"
# filename = "example"

# #四至，城市，中心经纬度
# lng_min = 121.467061
# lat_max = 31.376137
# lng_max = 121.990337
# lat_min = 30.849998

#爬取的间隔时间
# sleeptime = 8*60*60 #单位是秒，7200秒即为2小时

#是否使用fre自动设置cookie爬取次数 True Or False
AUTO_SET_FRE = True
#下面这个设置每个cookie抓取的次数(最好是线程数的倍数)
fre = 64

#每次爬取方格的边长（单位：km）
edge = 7.6

#下面的参数不用设置
lng_delta = 0.01167*edge
lat_delta = 0.009*edge