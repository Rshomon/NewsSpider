import scrapy
import re
from scrapy.loader import ItemLoader
from NewsSpider.items import ArticelItem
'''
蜻蜓新闻网
'''


class Vnn_cn_Spider(scrapy.Spider):
    name = 'Vnn_cn_Spider'
    allowed_domains = ['vnnb.cn/']
    start_urls = ['http://vnnb.cn/']

    def parse(self, response):
        link_url = response.xpath("//ul/li/a/@href").getall()
        link_url = list(map(lambda x: response.urljoin(x), link_url))
        for item in link_url:
            print(item)
        for url_item in link_url:
            if url_item != 'javascript:;':
                # 在进行二次request的时候，使用dont_filter=True，不用将request过滤掉
                yield scrapy.Request(url=url_item,
                                     callback=self.detail_parse,
                                     dont_filter=True)

    def detail_parse(self, response):
        # 使用ItemLoader管理存储的字段
        VnnCn_ItemLoader = ItemLoader(item=ArticelItem(), response=response)
        VnnCn_ItemLoader.add_xpath("detail_title", '//h1/span/text()')
        VnnCn_ItemLoader.add_xpath("release_time",
                                   "//div[@class='share_cnt_p']/i[1]/text()")
        VnnCn_ItemLoader.add_xpath("origin",
                                   "//div[@class='share_cnt_p']/i[2]")
        # TODO:文章内容需要处理 （拼接字符串并且替换文件中对于的字符）
        VnnCn_ItemLoader.add_xpath(
            "content",
            "//div[@class='J-contain_detail_cnt contain_detail_cnt']/p//text()"
        )
        vnncn_info = VnnCn_ItemLoader.load_item()
        print("下面输出使用ItemLoader管理的：")
        print(vnncn_info)
        # print("detail_title:%s\nrelease_time:%s\norigin:%s" %
        #       (detail_title, release_time, origin))
        # 获取是否有下一页
        next_page = response.xpath(
            "//div[@class='pagination']/li[last()]/a/@href").get()
        if next_page:
            if "#" in next_page:
                pass
            else:
                next_page_url = response.urljoin(next_page)
                print("*" * 30)
                print("存在下一页数据，继续爬取")

        else:
            # 没有下一页的数据了
            print("不存在下一页数据")
