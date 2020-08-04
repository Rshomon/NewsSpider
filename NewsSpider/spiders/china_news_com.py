# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urlencode
from NewsSpider.items import ArticelItem
"""
中国新闻网
"""


class ChinaNewsComSpider(scrapy.Spider):
    name = 'china_news_com'
    allowed_domains = ['chinanews.com']
    start_urls = ['http://www.bj.chinanews.com']
    num = 1

    def start_requests(self):
        # start_url = "http://www.bj.chinanews.com"
        # self.headers = {
        #     "Referer": "https://www.baidu.com/s?wd=%E6%96%B0%E9%97%BB%E7%BD%91&rsv_spt=1&rsv_iqid=0xcc4889b900013495&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=&tn=baiduhome_pg&ch=&rsv_enter=1&rsv_btype=i&rsv_dl=ib&inputT=5093",
        # }
        # yield scrapy.Request(url=start_url, headers=self.headers, callback=self.parse)

        self.param = {'q': '河南', 'dbtype': 'bj'}
        self.url = "http://search.news.chinanews.com/search.do" + "?" + urlencode(
            self.param)
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        # 获取每一个链接的地址
        url = re.findall(r'"url":"(http.+?html)', response.text)
        url_list = map(lambda x: x.replace("\\", ''), url)
        for item_url in url_list:
            yield scrapy.Request(item_url, callback=self.detail_parse)

        # url_list = response.xpath("//strong/a/@href").getall()
        # new_url_list = map(lambda x: response.urljoin(x), url_list)
        # for item_url in new_url_list:
        #     yield scrapy.Request(url=item_url, headers=self.headers, callback=self.detail_parse)
        if "下一页" in response.text:
            num = num + 1
            self.param['ps'] = 20
            self.param['start'] = num * 20

            self.param['time_scope'] = 0
            self.param['pubtime'] = ""
            url = "http://search.news.chinanews.com/search.do" + "?" + urlencode(
                self.param)
            yield scrapy.Request(url=url, callback=self.parse)

    '''
    解析詳情頁的內容
    '''

    def detail_parse(self, response):
        item = ArticelItem()
        # 标题
        title = response.xpath("//div//h1/text()").get()
        item['title'] = title
        # 时间
        push_time = re.findall(r'<span>(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2})',
                               response.text)[0]
        item['push_time'] = push_time
        # 来源
        origin = re.findall(r'来源：(.*?)</span>', response.text)[0]
        item['origin'] = origin
        # 内容
        detail_content = response.xpath(
            "//div[@class=' branch_con_text']/p//text()").getall()
        if isinstance(detail_content, list):
            detail_content = "".join(detail_content)
        item['detail_content'] = detail_content

        # print("title:%s\npush_time:%s\ndetail_content:%s\norigin:%s" %
        #       (title, push_time, detail_content, origin))
        return item
        # print(title)
