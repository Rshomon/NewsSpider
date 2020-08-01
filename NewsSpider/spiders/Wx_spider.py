import scrapy
from urllib.parse import urlencode
import re
import logging
import time
from scrapy.loader import ItemLoader
from NewsSpider.items import ArticelItem

from NewsSpider.spiders.log.init import Logger
logger = Logger()


class WxspiderSpider(scrapy.Spider):
    name = 'Wx_spider'
    allowed_domains = ['sogou.com']
    start_urls = ['http://sogou.com/']

    # def __init__(self):
    #     logging.basicConfig(level=logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #     self.logger = logging.getLogger(__name__)
    '''
    首次运行，用来加载新闻的列表页
    '''
    def start_requests(self):
        start_urls = "https://weixin.sogou.com/weixin?"
        param = {
            'type': '2',
            's_from': 'input',
            # 检索的关键字
            'query': '河南职业技术学院',
            'ie': 'utf8',
            '_sug_': 'n',
        }
        url = start_urls + urlencode(param)
        yield scrapy.Request(url=url, callback=self.parsea)

    '''
    获取列表中的@href，然后交由回掉处理
    需要解析两个数据，1：当前页面的详情页url。2:页数
    '''

    def parsea(self, response):
        headers = {
            "Host": "weixin.sogou.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language":
            "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        site_url = response.urljoin(
            response.xpath(
                "//div[@class='p-fy']/a[@id='sogou_next']/@href").get())
        if site_url:
            # 获取当前页面的下一页地址，重新解析
            yield scrapy.Request(url=site_url,
                                 callback=self.parsea,
                                 headers=headers)

        # 目标网址
        response_url = response.xpath(
            "//div[@class='txt-box']/h3/a/@href").getall()

        # 遍历获取到url，并添加完整
        for item_url in response_url:
            url = response.urljoin(item_url)
            # print(response_url)
            t = time.time()
            # 回调解析函数

            yield scrapy.Request(url=url,
                                 callback=self.analysis_url,
                                 meta={"time": t},
                                 headers=headers)

    def analysis_url(self, response):
        print("*" * 30)
        time_name = response.meta["time"]
        new_urlaaaaa = "".join(re.findall(r'url \+= \'(.*)\'', response.text))
        if new_urlaaaaa:
            print(new_urlaaaaa + "\n")
            yield scrapy.Request(new_urlaaaaa,
                                 callback=self.parse_detail,
                                 dont_filter=True)
        else:
            pass

    def parse_detail(self, response):
        # 正则匹配时间

        push1 = re.findall(r'\d{4}-\d{2}-\d{2}', response.text)
        logger.info("推送时间：" + "".join(push1))
        # TODO:使用ItemLoader接管字段处理,实例化
        WeixinspiderItemLoader = ItemLoader(item=ArticelItem(),
                                            response=response)
        # 使用正则匹配推送时间
        WeixinspiderItemLoader.add_xpath("push_time", push1)
        # 详情页标题
        WeixinspiderItemLoader.add_xpath("title",
                                         "//h2[@id='activity-name']/text()")

        # 详情页作者
        WeixinspiderItemLoader.add_xpath(
            "author",
            "//div[@id='meta_content']/span[@class='rich_media_meta rich_media_meta_text']/text()"
        )
        WeixinspiderItemLoader.add_value("push_time", push_date)
        # author = response.xpath(
        # "//div[@id='meta_content']/span[@class='rich_media_meta rich_media_meta_text']/text()"
        # ).get()
        # 来源
        # origin = response.xpath(
        #     "//div[@id='meta_content']/span[@id='profileBt']/a/text()").get()
        # try:
        #     origin = re.findall(
        #         re.findall(r'class="">来源 \| (.*)</', response.text)[0])
        # except:
        #     # self.logger.info("RE ERROR!")
        #     print("RE ERROR")
        # 推送时间

        # title = response.xpath("//h2[@id='activity-name']/text()").get()
        # 文章内容
        WeixinspiderItemLoader.add_xpath("//div[@id='js_content']//text()")

        weixin_info = WeixinspiderItemLoader.load_item()
        return weixin_info
        # detail_content = response.xpath("//section/section/p//text()").getall()
        # if not detail_content:
        #     detail_content = response.xpath(
        #         "//div[@class='rich_media_content']/p//text()").getall()

        # print("title:%s\nauthor:%s\ndetail_content:%s\n" %
        #       (title, author, detail_content))
