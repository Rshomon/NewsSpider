import scrapy


class MYidianSpider(scrapy.Spider):
    name = 'm_yidian'
    allowed_domains = ['go2yd.com']
    start_urls = ['http://www.go2yd.com']

    def start_requests(self):
        headers = {
            "Host":"a1.go2yd.com",
            "Cookie":"JSESSIONID=SjbcwUIztK5B67exm8i8WA",
            "apiname":"channel/news-list-for-keyword",
        }
        # url = "https://a1.go2yd.com/Website/channel/news-list-for-keyword?"+urlencode(param)
        url = 'https://a1.go2yd.com/Website/channel/news-list-for-keyword?word_type=token&eventid=120182403926fd6e9a-8baf-4dab-bab8-962915fb4838&ctype=overall&cstart=0&cend=30&display=%E8%8B%8F%E5%AE%81%E5%BF%AB%E9%80%92&fields=docid&signature=ckkaFLguPdH7J_0jFVtLttcQrqZFZQWVTF8CpGl-P9SLkAfb9uSHbNFg8qfYicpd6LIn2-KLkX3Xv-nep5T8c8KODfzydy9qE_YNZeJumTDPFb0_LbaFrS-uwkMbAjL3WijMuOK7WtZF59ZcuB_XGEDP0rLsMKW2s_pKI2sIqmQ&reqid=jvj9d3qv_1597204334222_1065&cv=5.4.6.0&appid=yidian'
        # logger.info(url)
        yield scrapy.Request(url=url,callback=self.parse,headers=headers)
    
    def parse(self,response):
        self.logger.info(response.body)