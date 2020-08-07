import os
import random
import requests
import logging

from scrapy.utils.project import get_project_settings
from NewsSpider.spiders.log.init import Logger
from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectionRefusedError
from twisted.web._newclient import ResponseNeverReceived
from scrapy.core.downloader.handlers.http11 import TunnelError
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)

settings = get_project_settings()


class UserAgentRandomMiddleware(object):
    def __init__(self):
        self.user_agent = settings['USER_AGENT']
        self.ua = UserAgent()

    def process_request(self, request, spider):
        # ua = random.choice(self.user_agent)
        # self.ua.random
        request.headers["User-Agent"] = self.ua.random
        # ua输出
        # logger.info("Current User-Agent:" + self.ua.random)


'''
检测代理是否可用
'''


def Check_proxy(proxy):
    pro = {'http': proxy}
    try:
        response = requests.get("https://www.sogou.com/",
                                proxies=pro,
                                timeout=2)
        logger.info("进入测试代理")
        if response.status_code == 200 or response.status_code == 302:
            logger.info("代理正常")
            return True
        else:
            return False
    except:
        return False


class ProxyRandomMiddleware(object):
    def __init__(self):
        # self.ALL_EXCEPTIONS = (TimeoutError, DNSLookupError,
        #               ConnectionRefusedError, ConnectionDone, ConnectError,
        #               ConnectionLost, TCPTimedOutError, ResponseFailed,

        #               IOError, TunnelError)
        self.ALL_EXCEPTIONS = (TimeoutError, ConnectionRefusedError,
                               ResponseNeverReceived, TCPTimedOutError,
                               TunnelError)
        # self.proxy_path = os.path.join(os.path.dirname(__file__),
        #                                'spiders\\utils\\proxy.log')
        # with open(self.proxy_path, 'r') as f:
        #     li = set()
        #     for item in f.readlines():
        #         li.add(item)
        #     self.pro_list = list(map(lambda x: x.replace("\n", ""), list(li)))
        self.request_url = settings["PROXYPOOL"]

    def process_request(self, request, spider):
        if request.meta.get('isProxy'):
            # 使用代理池获取proxy
            response = requests.get(self.request_url).text.strip()
            proxy = 'http://{}'.format(response)

            # proxy = random.choice(self.pro_list)
            # 设置是否重试
            # request.meta['dont_retry'] = True
            logger.info("Current Proxy:" + proxy)
            # if Check_proxy(proxy):
            request.meta["proxy"] = proxy
            #     return None
            # else:
            #     logger.info("响应无法")
            #     return request
        # return

    def process_response(self, request, response, spider):
        '''
        对返回的response处理
        如果返回的response状态不是200,重新生成当前request对象
        '''
        # if response.status != 200:
        if request.meta.get('proxy'):
            if response.status >= 400:
                logging.info("当前代理连接错误")
                return request
            else:
                logging.info("连接正常")
            return response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.ALL_EXCEPTIONS):
            logger.error("Got exception:%s" % (exception))
            return request

    # def process_exception(self, request, exception, spider):
    # # 捕获几乎所有的异常
    #     if isinstance(exception, self.ALL_EXCEPTIONS):
    #         # 在日志中打印异常类型
    #         logger.info('Got exception: %s' % (exception))
    #         # 重新请求
    #         return request


class ExceptionMiddleware(object):
    def __init__(self):
        self.ALL_EXCEPTIONS = (TimeoutError, ConnectionRefusedError,
                               ResponseNeverReceived, TCPTimedOutError,
                               TunnelError)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.ALL_EXCEPTIONS):
            logger.error("Got exception:%s" % (exception))
            return request
