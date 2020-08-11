'''
同时运行多个爬虫，使用crawler的CrawlerProcess类
'''
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

crawler = CrawlerProcess(settings)
crawler.crawl("Sogouengine")
crawler.crawl("Wx_spider")
crawler.crawl("Vnn_cn_Spider")
crawler.start()
crawler.start()
crawler.start()