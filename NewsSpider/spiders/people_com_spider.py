import scrapy


class PeoplespiderSpider(scrapy.Spider):
    name = 'people_com_spider'
    allowed_domains = ['people.com.cn/']
    start_urls = ['http://people.com.cn//']

    

    def start_requests(self):
        headers = {
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Host":
        "search.people.com.cn",
        "Referer":
        "http://search.people.com.cn/cnpeople/news/error.jsp",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    }
        data = {
            "siteName": "news",
            "pageNum": "1",
            "keyword": "%CB%D5%C4%FE",
            "facetFlag": "null",
            "originName": "",
            "pageCode": "",
            "nodeType": "belongsId",
            "nodeId": "0",
        }
        start_url = "http://search.people.com.cn/cnpeople/search.do"
        yield scrapy.FormRequest(url=start_url,
                                 formdata=data,
                                 headers=headers,
                                 callback=self.main_parse)
    def main_parse(self, response):
        print(response.url)