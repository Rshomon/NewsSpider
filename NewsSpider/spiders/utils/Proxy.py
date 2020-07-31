'''
    从代理池中获取可用代理
    主方法main()
'''
import requests, random
import time
import os

from concurrent.futures import ThreadPoolExecutor


class Proxy(object):
    def __init__(self):
        self.proxypool_url = [
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
            'http://127.0.0.1:5555/random',
        ]

    def get_random_proxy(self, url):
        """
        get random proxy from proxypool
        :return: proxy
        """
        return requests.get(url).text.strip()

    def crawl(self, proxy):
        url = 'http://httpbin.org/get'
        """
        use proxy to crawl page
        :param url: page url
        :param proxy: proxy, such as 8.8.8.8:8888
        :return: html
        """
        proxy1 = {}
        proxies = {'http': 'http://' + proxy}
        try:
            response = requests.get(url, proxies=proxies, timeout=3).text
            with open(os.path.join(os.path.dirname(__file__), 'proxy.log'),
                      'a') as f:
                f.write(proxies['http'] + '\n')
            return proxies["http"] + " connected"
        except:
            return proxies['http'] + " timeout"

    # @staticmethod
    def main(self):
        """ 
        main method, entry point
        :return: none
        """
        pro_list = []
        while True:
            with ThreadPoolExecutor(max_workers=20) as executor:
                for i in executor.map(self.get_random_proxy,
                                      self.proxypool_url):
                    print(i)
                    pro_list.append(i)

            with ThreadPoolExecutor(max_workers=20) as executor:
                for item in executor.map(self.crawl, pro_list):
                    print(item)
            pro_list = []
            print("Time sleep 2s")
            time.sleep(2)
        # pro_list = []

        # print('get random proxy', proxy)
        # html = self.crawl(self.target_url, proxy)
        # print(html)


if __name__ == "__main__":
    proxy = Proxy()
    proxy.main()