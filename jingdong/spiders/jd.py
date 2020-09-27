# -*- coding: utf-8 -*-
import re
import urllib.request

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import JingdongItem


class JdSpider(CrawlSpider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']

    rules = (
        Rule(LinkExtractor(allow=''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = JingdongItem()
        good_url = response.url
        pattern = r"item.jd.com/(.*?).html"
        match = re.search(pattern, good_url)

        if match:
            print(good_url)
            # print(response.text)
            good_id = re.compile(pattern).findall(good_url)[0].strip('/')
            good_name = response.xpath("//title/text()").extract_first()
            shop_name = response.xpath("//*[@id='crumb-wrap']/div/div[2]/div[2]/div[1]/div/a/text()").extract_first()
            shop_link = response.xpath("//@a[clstag='shangpin|keycount|product|dianpuname1']/@href").extract_first()

            comment_rate_url = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1".format(
                good_id)
            comment_count_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery5233766&_=1601117328101".format(
                good_id)
            good_price_url = "https://p.3.cn/prices/mgets?callback=jQuery4811902&type=1&area=21_1827_3502_0&pdtk=&pduid=100014589194&pdpin=&pin=null&pdbp=0&skuIds=J_{}%2CJ_10020572535473%2CJ_61490172556%2CJ_19149141140%2CJ_71954698755%2CJ_100009477910%2CJ_64059004718%2CJ_72307504732%2CJ_69852531542%2CJ_72017764925&ext=11100000&source=item-pc".format(
                good_id)

            comment_rate_resp = urllib.request.urlopen(comment_rate_url).read().decode('utf-8', 'ignore')
            comment_count_resp = urllib.request.urlopen(comment_count_url).read().decode('utf-8', 'ignore')
            good_price_resp = urllib.request.urlopen(good_price_url).read().decode('utf-8', 'ignore')

            comment_rate_pattern = r'.*?"goodRate":(.*?)'
            comment_count_pattern = r'.*?"CommentCount":(.*?)'
            good_price_pattern = r'.*?"p":"(.*?)","op"'

            comment_rate = re.compile(comment_rate_pattern).findall(comment_rate_resp)
            comment_count = re.compile(comment_count_pattern).findall(comment_count_resp)
            good_price = re.compile(good_price_pattern).findall(good_price_resp)[0]

            if good_name is not None:
                print(good_name, good_id, good_price)

        return item
