import scrapy
import time
import logging

from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter
from urllib.parse import urlencode
# logger = logging.getLogger(__name__)
# #第二步：修改日志的输出级别
# logger.setLevel(logging.DEBUG)

# #第三步：设置输出的日志内容格式
# fmt = "%(log_color)s%(asctime)s  %(log_color)s%(filename)s  %(log_color)s%(funcName)s [line:%(log_color)s%(lineno)d] %(log_color)s%(levelname)s %(log_color)s%(message)s"
# datefmt = '%a, %d %b %Y %H:%M:%S'

# formatter = ColoredFormatter(fmt=fmt,
#                              datefmt=datefmt,
#                              reset=True,
#                              log_colors={
#                                  'DEBUG': 'cyan',
#                                  'INFO': 'green',
#                                  'WARNING': 'yellow',
#                                  'ERROR': 'red',
#                                  'CRITICAL': 'red,bg_white'
#                              },
#                              secondary_log_colors={},
#                              style='%')

# #设置输出渠道--输出到控制台
# hd_1 = logging.StreamHandler()
# #在handler上指定日志内容格式
# hd_1.setFormatter(formatter)

# #第五步：将headler添加到日志logger上
# logger.addHandler(hd_1)


class SogouengineSpider(scrapy.Spider):
    name = 'Sogouengine'
    allowed_domains = ['sogou.com']
    start_urls = ['http://sogou.com/']
    """ 解析搜狗搜索地址，传入参数 """
    def start_requests(self):
        start_url = "https://www.sogou.com/sogou?"
        params = {
            "query": "河南职业技术学院",
            "_ast": str(int(time.time())),
            "_asf": "www.sogou.com",
            "w": "01029901",
            "pid": "sogou-wsse-8f646834ef1adefa",
            "duppid": "1",
            "p": "40230447",
            "dp": "1",
            "cid": "",
            "interation": "1728053249",
            "s_from": "result_up",
        }
        url = start_url + urlencode(params)
        headers = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "Referer": url,
            'Host': "www.sogou.com"
        }
        yield scrapy.Request(url, callback=self.parse, headers=headers)

    """ 列表页，如果存在下一页，再次回调 """

    def parse(self, response):
        if "用户您好，我们的系统检测到您网络中存在异常访问请求。" in response.text:
            logging.warning("网络异常！"+"=" * 30)
            return
        url = response.xpath("//div[@class='vrwrap']//h3/a/@href").getall()
        for item in url:
            yield scrapy.Request(response.urljoin(item),
                                 callback=self.detail_parse)
        if "下一页" in response.text:
            next_url = response.xpath("//a[@id='sogou_next']/@href").get()
            yield scrapy.Request(response.urljoin(next_url), self.parse)

    def detail_parse(self, response):

        logging.warning("已经入详情页，获取url"+"*" * 30)
        logging.warning(response.url)
