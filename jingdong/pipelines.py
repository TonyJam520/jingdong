# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class JingdongPipeline:
    def process_item(self, item, spider):
        db = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            db='jd'
        )
        cursor = db.cursor()
        print(item)
        sql1 = "insert into goods values (%s,%s,%s,%s,%s)"
        sql2 = "insert into shop(shop_link, shop_name, shop_goods_score, shop_after_sale_service_score, shop_logistics_service_score) values (%s,%s,%s,%s,%s)"
        for i in range(0, len(item['goods_id'])):
            try:
                dd1 = [item['goods_id'], item['goods_name'], item['goods_price'], item['comment_rate'],
                       item['comment_count']]
                dd2 = [item['shop_link'], item['shop_name'], item['shop_goods_score'],
                       item['shop_after_sale_service_score'], item['shop_logistics_service_score']]
                cursor.execute(sql1, dd1)
                cursor.execute(sql2, dd2)
                print("success")
            except Exception as e:
                item.clear()
                print('Duplicated.')
                print(e)
        db.commit()

        return item
