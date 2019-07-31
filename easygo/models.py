import requests
import json
import os
import time
import yaml

from easygo import settings

from selenium import webdriver
from requests.exceptions import RequestException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class proxyObject(object):
    """proxy类：用于获取proxy"""

    def get_proxy_txt(self):
        while True:
            try:
                webdata = requests.get(settings.proxy_url)
                if webdata.status_code == 200:
                    print("get new proxy:{}".format(webdata.text.split(",")[0]))
                    return "http://"+webdata.text.split("\n")[0].split(",")[0]
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
    qq_list = []
    qq_number_sides = settings.qq_number_sides

    def remove_cookie(self, banned_cookie):
        self.cookies.remove(banned_cookie)

    def get_track(self, distance):      # distance为传入的总距离
        distance += 20
        # 移动轨迹
        track=[]
        # 当前位移
        current=0
        # 减速阈值
        mid=distance*3/5
        # 计算间隔
        t=0.2
        # 初速度
        v=0        
        while current<distance:
            if current<mid:
                # 加速度为2
                a=2
            else:
                # 加速度为-2
                a=-3
            v0=v
            # 当前速度
            v=v0+a*t
            # 移动距离
            move=v0*t+1/2*a*t*t
            # 当前位移
            current+=move
            # 加入轨迹
            track.append(round(move))
            back_tracks = [-1, -1, -1, -2, -3, -2, -2, -2, -2, -1, -1, -1]
        #return track
        return {'track':track, 'back_tracks':back_tracks}

    def move_to_gap(self, chrome_login, slider, tracks):     # slider是要移动的滑块,tracks是要传入的移动轨迹
        ActionChains(chrome_login).click_and_hold(slider).perform()
        for x in tracks['track']:
            ActionChains(chrome_login).move_by_offset(xoffset=x,yoffset=0).perform()
        time.sleep(0.3)

        for back_track in tracks['back_tracks']:
            ActionChains(chrome_login).move_by_offset(xoffset=back_track, yoffset=0).perform()
        ActionChains(chrome_login).release().perform()
        time.sleep(0.3)

    def acquire_cookies(self):
        qqlist_filename = settings.qq_list
        with open(qqlist_filename, 'r') as f:
            self.qq_list = yaml.load(f)
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
                if settings.USE_PROXY_LOGIN == True:
                    proxyO = proxyObject()
                    chrome_proxy = proxyO.get_proxy_txt()
                    chromeOptions.add_argument('--proxy-server={}'.format(chrome_proxy))
                chromedriver = r'./chromedriver'
                # os.environ["webdriver.chrme.driver"] = chromedriver
                chrome_login = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
                chrome_login.get("https://ui.ptlogin2.qq.com/cgi-bin/login?pt_hide_ad=1&style=9&appid=549000929&pt_no_auth=1&pt_wxtest=1&daid=5&s_url=https%3A%2F%2Fh5.qzone.qq.com%2Fmqzone%2Findex")
                try:
                    num = qq_number_side
                    qq_num = self.qq_list[num][0]
                    qq_passwd = self.qq_list[num][1]
                    print(qq_num)
                except IndexError as e:
                    pass
                
                try:
                    chrome_login.find_element_by_id("u").send_keys(str(qq_num))
                    chrome_login.find_element_by_id("p").send_keys(str(qq_passwd))
                    chrome_login.maximize_window()
                    chrome_login.find_element_by_id("go").click()
                except Exception as e:
                    chrome_login.quit()
                    continue
                
                # 如有滑块验证拖动滑块
                # 10秒内判断元素是否出现
                # try:
                #     element = WebDriverWait(chrome_login, 20).until(
                #         EC.presence_of_element_located((By.ID, "transform_eh"))
                #     )
                # except Exception as e:
                #     driver.quit()
                #     continue
                # time.sleep(20)
                while (chrome_login.current_url=="https://ui.ptlogin2.qq.com/cgi-bin/login?pt_hide_ad=1&style=9&appid=549000929&pt_no_auth=1&pt_wxtest=1&daid=5&s_url=https%3A%2F%2Fh5.qzone.qq.com%2Fmqzone%2Findex"):
                    time.sleep(3)
                    if settings.AUTO_CAPTCHA == True:
                        if "安全验证" in chrome_login.page_source:
                            try:
                                chrome_login.switch_to_frame('tcaptcha_iframe')
                                button = chrome_login.find_element_by_xpath("//div[@id='tcaptcha_drag_thumb']")                  
                                self.move_to_gap(chrome_login, button, self.get_track(196))             
                            except Exception as e:
                                print('failed', e)
                
                    # 当遇到qq号不能登录时，手动输入其他qq号
                    # if ("你输入的帐号或密码不正确，请重新输入。"or"为了账号安全，请使用一键登录。" in chrome_login.page_source) and (chrome_login.current_url=="https://ui.ptlogin2.qq.com/cgi-bin/login?pt_hide_ad=1&style=9&appid=549000929&pt_no_auth=1&pt_wxtest=1&daid=5&s_url=https%3A%2F%2Fh5.qzone.qq.com%2Fmqzone%2Findex"):
                    #     chrome_login.quit()
                    #     qq_number_side = int(input('登录错误，请输入其他QQ号再次尝试：'))
                    #     break
                                        
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