# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TencentArticle(scrapy.Item):
    flag = scrapy.Field()
    news_id = scrapy.Field()
    parent_name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    comments_id = scrapy.Field()
    comments_url = scrapy.Field()
    comments_number = scrapy.Field()


class TencentComment(scrapy.Item):
    flag = scrapy.Field()
    news_id = scrapy.Field()
    comments_id = scrapy.Field()
    username = scrapy.Field()
    comment = scrapy.Field()
    datetime = scrapy.Field()
    sex = scrapy.Field()
    reply_id = scrapy.Field()
    agree_count = scrapy.Field()	
