# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Join, Compose


class ArticelItem(scrapy.Item):
    # define the fields for your item here like:
    # _id = scrapy.Field()
    # 文章标题
    title = scrapy.Field(output_processor=TakeFirst())
    # 推送时间
    push_time = scrapy.Field(output_processor=TakeFirst())
    # 作者信息
    author = scrapy.Field(output_processor=TakeFirst())
    # 文章来源
    origin = scrapy.Field(output_processor=TakeFirst())
    # 详情页地址
    url = scrapy.Field(output_processor=TakeFirst())
    # 文章详情
    detail_content = scrapy.Field(input_processor=Join(),
                                  outout_processor=TakeFirst())


class SiteItem(scrapy.Item):
    # title
    title = scrapy.Field()
    # url
    url = scrapy.Field()