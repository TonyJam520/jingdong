#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random

page_url = "http://dev.kdlapi.com/testproxy"  # 要访问的目标网页
# API接口，返回格式为json
api_url = "https://dps.kdlapi.com/api/getdps/?orderid=940241765382312&num=1&pt=1&format=json&sep=1"

# API接口返回的ip
proxy_ip = requests.get(api_url).json()['data']['proxy_list']
print(proxy_ip)

# 用户名密码认证(私密代理/独享代理)
username = "52051345"
password = "cud72i77"

proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password, 'proxy': random.choice(proxy_ip)},
    "https": "https://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password, 'proxy': random.choice(proxy_ip)}
}
print(proxies)
headers = {
    "Accept-Encoding": "Gzip",  # 使用gzip压缩传输数据让访问更快
}
r = requests.get(page_url, proxies=proxies, headers=headers)
print(r.status_code)  # 获取Response的返回码

if r.status_code == 200:
    r.enconding = "utf-8"  # 设置返回内容的编码
    print(r.content)  # 获取页面内容