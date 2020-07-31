import scrapy


class NewspiderSpider(scrapy.Spider):
    name = 'NewSpider'
    allowed_domains = ['cd ..']
    start_urls = ['http://cd ../']

    def parse(self, response):
        pass
