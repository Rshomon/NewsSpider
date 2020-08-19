import sys
from NewsSpider.loadJson import get_config
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
"""
通用爬虫的入口
"""


def run():
    name = sys.argv[1]
    custom_settings = get_config(name)
    # 爬虫名
    spider = custom_settings.get("spider")
    process = CrawlerProcess(settings)
    process.crawl(spider, **{"name": name})
    process.start()


if __name__ == "__main__":
    run()
