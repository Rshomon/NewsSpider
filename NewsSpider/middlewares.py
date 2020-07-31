import os
import random
import requests
import logging

from scrapy.utils.project import get_project_settings
from NewsSpider.spiders.log.init import Logger
from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectionRefusedError
from twisted.web._newclient import ResponseNeverReceived
from scrapy.core.downloader.handlers.http11 import TunnelError
 
logger = logging.getLogger(__name__)


class UserAgentRandomMiddleware(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.user_agent = self.settings['USER_AGENT']

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent)
        request.headers["User-Agent"] = ua
        logger.info("Current User-Agent:" + ua)


class ProxyRandomMiddleware(object):
    def __init__(self):
        # self.ALL_EXCEPTIONS = (TimeoutError, DNSLookupError,
        #               ConnectionRefusedError, ConnectionDone, ConnectError,
        #               ConnectionLost, TCPTimedOutError, ResponseFailed,
        #               IOError, TunnelError)
        self.proxy_path = os.path.join(os.path.dirname(__file__),
                                       'spiders\\utils\\proxy.log')
        with open(self.proxy_path, 'r') as f:
            li = set()
            for item in f.readlines():
                li.add(item)
            self.pro_list = list(map(lambda x: x.replace("\n", ""), list(li)))

    def process_request(self, request, spider):
        proxy = random.choice(self.pro_list)
        request.meta["proxy"] = proxy
        logger.info("Current Proxy:" + proxy)

    def process_response(self, request, response, spider):
        '''
        对返回的response处理
        如果返回的response状态不是200,重新生成当前request对象
        '''
        if response.status != 200:
            proxy = random.choice(self.pro_list)
            request.meta['proxy'] = proxy
            return request
        return response

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


if __name__ == '__main__':
    main()