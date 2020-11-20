# -*- coding: utf-8 -*-
import re
import urllib.request

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import JingdongItem
from ..my_proxies import ProxyPool


class JdSpider(CrawlSpider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']

    def __init__(self):
        super(JdSpider, self).__init__()
        my_proxy_pool = ProxyPool()
        my_proxy_pool.main()

    rules = (
        Rule(LinkExtractor(allow=''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = JingdongItem()
        good_url = response.url
        pattern = r"item.jd.com/(.*?).html"
        match = re.search(pattern, good_url)

        if match:
            # 商品id
            goods_id = re.compile(pattern).findall(good_url)[0].strip('/')
            # 商品名
            goods_name = response.xpath("//title/text()").extract_first()
            # 店铺名
            shop_name = response.xpath("//*[@id='crumb-wrap']/div/div[2]/div[2]/div[1]/div/a/text()").extract_first()
            # 店铺链接
            shop_link = 'http:' + response.xpath("//*[@id='crumb-wrap']/div/div[2]/div[2]/div[1]/div/a/@href").extract_first()
            shop_goods_score = ""
            shop_after_sale_service_score = ""
            shop_logistics_service_score = ""
            try:
                # 店铺商品总评分
                shop_goods_score_string = response.xpath("//*[@id='crumb-wrap']/div/div[2]/div[2]/div[6]/div/div/div[1]/a[1]/div[2]/em/text()").extract_first()
                shop_goods_score_pattern = r".*?(\d+\.\d+).*?"
                shop_goods_score = re.compile(shop_goods_score_pattern).findall(str(shop_goods_score_string))[0]
                # 售后服务评分
                shop_after_sale_service_score_string = response.xpath("//*[@id='crumb-wrap']/div/div[2]/div[2]/div[6]/div/div/div[1]/a[3]/div[2]/em/text()").extract_first()
                shop_after_sale_service_score_pattern = r".*?(\d+\.\d+).*?"
                shop_after_sale_service_score = re.compile(shop_after_sale_service_score_pattern).findall(str(shop_after_sale_service_score_string))[0]
                # 物流服务评分
                shop_logistics_service_score_string = response.xpath("//*[@id='crumb-wrap']/div/div[2]/div[2]/div[6]/div/div/div[1]/a[2]/div[2]/em/text()").extract_first()
                shop_logistics_service_score_pattern = r".*?(\d+\.\d+).*?"
                shop_logistics_service_score = re.compile(shop_logistics_service_score_pattern).findall(str(shop_logistics_service_score_string))[0]
            except IndexError:
                pass

            comment_rate_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery5233766&_=10141187361".format(
                goods_id)
            comment_count_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery5233766&_=10141187361".format(
                goods_id)
            good_price_url = "https://p.3.cn/prices/mgets?callback=jQuery4811902&type=1&area=21_1827_3502_0&pdtk=&pduid=100014589194&pdpin=&pin=null&pdbp=0&skuIds=J_{}%2CJ_10020572535473%2CJ_61490172556%2CJ_19149141140%2CJ_71954698755%2CJ_100009477910%2CJ_64059004718%2CJ_72307504732%2CJ_69852531542%2CJ_72017764925&ext=11100000&source=item-pc".format(
                goods_id)

            comment_rate_resp = urllib.request.urlopen(comment_rate_url).read().decode('utf-8', 'ignore')
            comment_count_resp = urllib.request.urlopen(comment_count_url).read().decode('utf-8', 'ignore')
            goods_price_resp = urllib.request.urlopen(good_price_url).read().decode('utf-8', 'ignore')

            comment_rate_pattern = r'.*?tStr.*?GoodRate":(.*?),"GoodRat'
            comment_count_pattern = r'.*?CommentCount":(.*?),"Averag'
            good_price_pattern = r'.*?"p":"(.*?)","op"'
            # 好评率
            comment_rate = re.compile(comment_rate_pattern).findall(comment_rate_resp)[0]
            # 好评数量
            comment_count = re.compile(comment_count_pattern).findall(comment_count_resp)[0]
            # 商品价格
            goods_price = re.compile(good_price_pattern).findall(goods_price_resp)[0]

            item['goods_id'] = goods_id
            item['goods_name'] = goods_name
            item['goods_price'] = goods_price
            item['comment_rate'] = comment_rate
            item['comment_count'] = comment_count
            item['shop_name'] = shop_name
            item['shop_link'] = shop_link
            item['shop_goods_score'] = shop_goods_score
            item['shop_after_sale_service_score'] = shop_after_sale_service_score
            item['shop_logistics_service_score'] = shop_logistics_service_score

            if goods_id is not None:
                yield item
