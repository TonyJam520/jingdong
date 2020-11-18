# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field()
    goods_name = scrapy.Field()
    goods_price = scrapy.Field()
    comment_rate = scrapy.Field()
    comment_count = scrapy.Field()
    shop_name = scrapy.Field()
    shop_link = scrapy.Field()
