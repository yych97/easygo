from scrapy import cmdline
import time
import schedule
from easygo import settings
import yaml
import os

def job(use_qq):
    qq_list_all = []
    qqlist_all_filename = settings.qq_list_all
    qqlist_filename = settings.qq_list
    cookie_file = settings.cookie_file
    # 检查临时文件存在与否，存在则删除
    if os.path.exists(qqlist_filename):
        os.remove(qqlist_filename)
    if os.path.exists(cookie_file):
        os.remove(cookie_file)
    # 生成运行临时文件
    with open(qqlist_all_filename, 'r') as f:
        qq_list_all = yaml.load(f, Loader=yaml.FullLoader)
    with open(qqlist_filename, 'w') as f:
        qq_list = []
        for num in use_qq:
            qq_list.append(qq_list_all[num])
        yaml.dump(qq_list, f)
    cmdline.execute('scrapy crawl easygo_spider'.split())

# schedule.every().day.at("06:00").do(job, [0, 1])
# schedule.every().day.at("07:00").do(job, [2, 3])
# schedule.every().day.at("08:00").do(job, [4, 5])
# schedule.every().day.at("09:00").do(job, [6, 7])

# schedule.every().day.at("14:00").do(job, [2, 3])
# schedule.every().day.at("15:00").do(job, [4, 5])
# schedule.every().day.at("16:00").do(job, [6, 7])
# schedule.every().day.at("17:00").do(job, [8, 9])

job([3, 4])

# while True:
#     schedule.run_pending()
#     time.sleep(30)

# cmdline.execute('scrapy crawl easygo_spider'.split())
# cmdline.execute('scrapy crawl httpbin'.split())