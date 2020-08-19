import scrapy
import json
from NewsSpider.spiders.utils.Itemutil import ProductLoader
from scrapy.loader import ItemLoader
from NewsSpider.items import ArticelItem
from NewsSpider.loadJson import get_config


class UniversalSpider(scrapy.Spider):
    name = "universal"

    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.name = config.get("spider")
        self.start_urls = config.get("start_url")
        self.allowed_domains = config.get("allowed_domains")
        # 执行父类构造构造函数
        super(UniversalSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        next_page = self.config.get("next_page")
        # self.logger.info(eval(next_page.get("Isnext")))
        if eval(next_page.get("Isnext")):
            # 存在下一页继续发送请求
            if next_page.get("next_url").get("pattern") == "xpath":
                next_url = response.xpath(
                    next_page.get("next_url").get("args")).get()
                if next_url:
                    self.logger.info("存在下一页，继续发送请求")
                    # yield scrapy.Request(url=response.urljoin(next_url),
                    #  callback=self.parse)
        # 遍历每一条的详情页

        url = response.xpath(
            self.config.get("page_list_url").get("args")).getall()
        for item_url in url:
            self.logger.info("进入详情页")
            yield scrapy.Request(url=item_url, callback=self.detail_parse)

    def detail_parse(self, response):
        item = self.config.get("item")
        cls = eval(item.get("class"))()
        loader = eval(item.get("loader"))(cls, response=response)
        for key, value in item.get("attrs").items():
            if value.get("pattern") == "xpath":
                loader.add_xpath(key, value.get("args"))
            if value.get("pattern") == "value":
                loader.add_value(key, response.url)
        yield loader.load_item()