# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
from easygo import settings
from scrapy.exporters import CsvItemExporter

class EasygoPipeline(object):
    def __init__(self):
        time_now = time.time()
        time_now_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time_now))
        file_name = settings.filepath + time_now_str + ".csv"
        self.fp = open(file_name, 'wb')
        self.exporter = CsvItemExporter(self.fp, encoding='utf-8')
        self.exporter.start_exporting()

    def open_spider(self, spider):
        print('start')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()
        print('finish')

    # 自定义函数
    def remove_duplicate(self, filepath):
        res = {}
        res_ = []
        with open(filepath,'r',encoding='utf-8') as f:
            read_res = f.readlines()[1:]
            length = len(read_res)
            for item in enumerate(read_res):
                count,lng,lat,time = item[1].strip().split(",")
                res[(lng,lat)] = (count,time)
                sys.stdout.write("\r{0},{1}".format(item[0],length))
                sys.stdout.flush()
        for item in res.items():
            lng,lat = item[0]
            count,time = item[1]
            data = {"lng":lng,
                    "lat":lat,
                    "count":count,
                    "time":time}
            res_.append(data)
        df = pandas.DataFrame(res_)

        csv_name = filepath.replace(".txt","去重结果.csv")
        df.to_csv(csv_name,index = False)
