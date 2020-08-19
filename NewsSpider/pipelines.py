# useful for handling different item types with a single interface
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import json
import pymongo
from scrapy.exporters import JsonItemExporter
from scrapy.utils.project import get_project_settings
import copy


class NewsSpiderPipeline(object):
    def process_item(self, item, spider):
        logging.info(dict(item))
        return item


class SogouSpiderPipeline(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.port = self.settings['MONGODB_PORT']
        self.host = self.settings['MONGODB_HOST']
        self.db = self.settings['MONGODB_DB']

        # self.file = open('ArticleInfo.json', 'ab')
        # self.exporter = JsonItemExporter(self.file,
        #                                  ensure_ascii=False,
        #                                  encoding="utf-8")
        # # 开启数据存储（json）
        # self.exporter.start_exporting()
        # 开启mongodb连接
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.db]
        self.info = self.db['newsinfo']

    # 爬虫开启时调用

    def open_spider(self, spider):
        print('爬虫开启')
# 存储相关操作

    def process_item(self, item, spider):
        # self.exporter.export_item(item)
        item_dic = {}
        # item = ItemAdapter(item)
        item_input = copy.deepcopy(item)
        # 处理长篇文章的输出
        content = item_input.get("detail_content", None)
        if content != None:
            content = "".join(content)[:30] + "......"
        # logging.info(f"title:{item_input['title']}\npush_time:{item_input['push_time']}\n")
        item_input['detail_content'] = content

        item_dic['title'] = item_input.get("title", None)
        item_dic['push_time'] = item_input.get("push_time", None)
        item_dic['author'] = item_input.get("author", None)
        item_dic['url'] = item_input.get("url", None)
        item_dic['detail_content'] = content
        logging.info(f'{item_input}')
        # logging.info(item)
        # 入库
        self.info.insert_one(dict(item))
        return item


# 爬虫关闭时调用

    def close_spider(self, spider):
        print("爬虫关闭")
        # 关闭数据存储（json）
        # self.exporter.finish_exporting()
        # self.file.close()
