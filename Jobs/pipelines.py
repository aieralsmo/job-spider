# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class Job51Pipeline(object):
    def process_item(self, item, spider):

        with open('51job-data.json', 'a',encoding="UTF-8") as f:
            data = json.dumps(dict(item),ensure_ascii=False,indent=4)
            f.write(data)
        return item


class ZhaopinPipeline(object):
    def process_item(self, item, spider):

        with open('zhaopin-data.json', 'a',encoding="UTF-8") as f:
            data = json.dumps(dict(item),ensure_ascii=False,indent=4)
            f.write(data)
        return item


class HuiboPipeline(object):
    def process_item(self, item, spider):

        with open('huibo-data.json', 'a',encoding="UTF-8") as f:
            data = json.dumps(dict(item),ensure_ascii=False,indent=4)
            f.write(data+",")
        return item