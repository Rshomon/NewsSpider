import scrapy
import json


class UniversalSpider(scrapy.Spider):
    name = 'universal'
    allowed_domains = ['xiaomi.cn']
    start_urls = [
        'https://prod.api.xiaomi.cn/community/square?start=&limit=10'
    ]
    headers = {
        "Host":
        "prod.api.xiaomi.cn",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    }

    def parse(self, response):
        response = json.loads(response.text)
        if response != "":
            result = response['entity']['records']
            for item in range(2):
                id = result[item].get("id", '为获取到标题')
                url = 'https://www.xiaomi.cn/post/' + id
                yield scrapy.Request(url=url,
                                     callback=self.detail_parse,
                                     headers=self.headers,
                                     dont_filter=True)

    def detail_parse(self, response):
        self.logger.info(response.body)
        # title = response.xpath("//div//h1/text()").get()
        # author = response.xpath("//div[@class='author-name']/text()").get()
        # info = response.xpath(
        #     "//div[@class='author-info-bottom']/text()").get()
        # content = response.xpath("//article//p/text()").getall()
        # self.logger.info(f'{title}\n{author}\n{info}\n{content}')