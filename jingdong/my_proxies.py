# -*- coding: utf-8 -*-
from threading import Thread

import requests

from fake_useragent import UserAgent


PROXY = []
# 这里是快代理私密代理提取ip的账号和密码
username = "uasername"
password = "password"


class ProxyPool(object):
    # API接口，返回格式为json
    api_url = "https://dps.kdlapi.com/api/getdps/?orderid=940241765382312&num=1&pt=1&format=json&sep=1"
    # 用户名密码认证(私密代理/独享代理)
    proxy_ip_list = []

    def get_user_agent(self):
        return UserAgent().random

    def get_headers(self):
        return {'User-Agent': self.get_user_agent()}

    def check_proxies(self, proxy_ip):
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password,
                                                            'proxy': proxy_ip},
            "https": "https://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password,
                                                              'proxy': proxy_ip},
            'no': '192.168.99.100'
        }
        try:
            req = requests.get(url='http://httpbin.org/get', proxies=proxies, headers=self.get_headers(), timeout=10)
            print(req.text)
        except Exception as e:
            print(str(proxy_ip) + ' is invalid and now has been removed.')
            self.proxy_ip_list.remove(proxy_ip)

    def create_proxy_ip_pool_from_remote(self):
        proxy_ip = requests.get(self.api_url).json()['data']['proxy_list']
        self.proxy_ip_list.extend(proxy_ip)

    def create_proxies_pool_from_local(self):
        with open(r'C:\GitHub\jingdong\jingdong\proxies.txt', 'r') as file:
            for line in file.readlines():
                if len(line) > 0:
                    self.proxy_ip_list.append(line.strip())

    def save_proxy_ip(self):
        with open(r'C:\GitHub\jingdong\jingdong\proxies.txt', 'w') as file:
            if len(self.proxy_ip_list) > 0:
                for proxy_ip in self.proxy_ip_list:
                    file.write(str(proxy_ip) + '\n')

    def main(self):
        self.create_proxies_pool_from_local()
        thread_list = []
        for proxy_ip in self.proxy_ip_list:
            thread = Thread(target=self.check_proxies, args=(proxy_ip,))
            thread_list.append(thread)
            thread.start()
        for thread in thread_list:
            thread.join()
        if len(self.proxy_ip_list) < 3:
            self.create_proxy_ip_pool_from_remote()
        PROXY.extend(self.proxy_ip_list)
        print(PROXY)
        self.save_proxy_ip()


# if __name__ == '__main__':
#     my_proxy_pool = ProxyPool()
#     my_proxy_pool.main()
