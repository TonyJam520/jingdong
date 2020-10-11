import time
from threading import Thread
import urllib3

import requests

from fake_useragent import UserAgent
from lxml import etree

PROXY = []

class ProxyPool:

    def __init__(self):
        self.proxy_list = []
        self.url = "https://www.kuaidaili.com/free/intr/{}/"

    def get_user_agent(self):
        return UserAgent().random

    def get_headers(self):
        return {'User-Agent': self.get_user_agent()}

    def create_proxy_list(self):
        headers = self.get_headers()
        for i in range(1, 5):
            real_url = self.url.format(i)
            # print(real_url)
            html = requests.get(url=real_url, headers=headers, verify=False).content.decode('utf-8')
            xml = etree.HTML(html)
            ip_list = xml.xpath("//tr/td[@data-title='IP']/text()")
            port_list = xml.xpath("//tr/td[@data-title='PORT']/text()")
            # print(ip_list, port_list)
            # print(len(ip_list), len(port_list))
            time.sleep(1)  # 这里测试发现快代理会检测请求速度，延迟一秒请求，否则获取不到
            for j in range(0, len(ip_list)):
                self.proxy_list.append(ip_list[j] + ':' + port_list[j])

    def check_proxy(self, proxy):
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        headers = self.get_headers()
        target_url = "http://jd.com"

        # noinspection PyBroadException
        try:
            # 由于这里我们使用了多线程，同一时间发送的请求太多，所以timeout时间设置长一点
            requests.get(url=target_url, headers=headers, proxies=proxies, timeout=10)
        except Exception as e:
            print(proxy + " is invalid and now it's removed.")
            self.proxy_list.remove(proxy)

    def create_proxy_pool(self):
        thread_list = []
        for proxy in self.proxy_list:
            thread = Thread(target=self.check_proxy, args=(proxy,))
            thread.start()
            thread_list.append(thread)
            time.sleep(0.1)
        for thread in thread_list:
            thread.join()

    def main(self):
        self.create_proxy_list()
        self.create_proxy_pool()


# if __name__ == '__main__':
#     urllib3.disable_warnings()
#     MyProxyPool = ProxyPool()
#     MyProxyPool.main()
#     print("After filtering, the following {} proxies is useful.".format(len(MyProxyPool.proxy_list)))
#     for proxy in MyProxyPool.proxy_list:
#         print(proxy)
