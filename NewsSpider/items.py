# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticelItem(scrapy.Item):
    # define the fields for your item here like:
    # _id = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 推送时间
    push_time = scrapy.Field()
    # 作者信息
    author = scrapy.Field()
    # 文章来源
    origin = scrapy.Field()
    # 文章详情
    detail_content = scrapy.Field()


class SiteItem(scrapy.Item):
    # title
    title = scrapy.Field()
    # url
    url = scrapy.Field()