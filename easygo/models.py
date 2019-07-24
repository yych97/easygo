import requests
import json
import os
import time

from easygo import settings

from selenium import webdriver
from requests.exceptions import RequestException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver import ActionChains

class proxyObject(object):
    """proxy类：用于获取proxy"""

    def get_proxy_txt(self):
        while True:
            try:
                webdata = requests.get(settings.proxy_url)
                if webdata.status_code == 200:
                    print("get new proxy:{}".format(webdata.text.split(",")[0]))
                    return "http://"+webdata.text.split(",")[0]
            except Exception as e:
                print("get new proxy failed " + str(e.args))

    def get_proxy_json(self):
        while True:
            try:
                res = requests.get(settings.proxy_url)
                if res.status_code == 200:
                    webdata = json.loads(res.text)
                    code = webdata['code']
                    success = webdata['success']
                    msg = webdata['msg']
                    data = webdata['data'][0]
                    ip = data['ip']
                    port = data['port']
                    expire_time = data['expire_time']
                    city = data['city']
                    print("get new proxy:{}:{}".format(ip, port))
                    return "https://{}:{}".format(ip, port)
            except Exception as e:
                print("get new proxy failed " + str(e.args))


class cookieObject(object):
    """cookie类：用于模拟登录获取cookie"""
    cookies = []
    qq_number_sides = settings.qq_number_sides

    def remove_cookie(self, banned_cookie):
        self.cookies.remove(banned_cookie)

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