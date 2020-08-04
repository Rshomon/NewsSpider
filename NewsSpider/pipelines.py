# useful for handling different item types with a single interface
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import json
from scrapy.exporters import JsonItemExporter


class NewsSpiderPipeline(object):
    def process_item(self, item, spider):
        logging.info(dict(item))
        return item


class SogouSpiderPipeline(object):
    def __init__(self):
        self.file = open('ArticleInfo.json', 'ab')
        self.exporter = JsonItemExporter(self.file,
                                         ensure_ascii=False,
                                         encoding="utf-8")
        # 开启数据存储（json）
        self.exporter.start_exporting()

    # 爬虫开启时调用

    def open_spider(self, spider):
        print('爬虫开启')
# 存储相关操作

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        logging.info(item)
        return item


# 爬虫关闭时调用

    def close_spider(self, spider):
        print("爬虫关闭")
        # 关闭数据存储（json）
        self.exporter.finish_exporting()
        self.file.close()
