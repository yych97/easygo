import requests
import json
from easygo import settings

class proxyObject(object):
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