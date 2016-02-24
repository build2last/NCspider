# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SohuArticle(scrapy.Item):
    flag = scrapy.Field()
    news_id = scrapy.Field()
    title= scrapy.Field()
    time= scrapy.Field()
    comments_number = scrapy.Field(default=0)
    content = scrapy.Field()
    news_url=scrapy.Field()	

class SohuComment(scrapy.Item):
    flag = scrapy.Field()
    news_id = scrapy.Field()
    comments_id = scrapy.Field()
    author = scrapy.Field()
    comment = scrapy.Field()
    datetime = scrapy.Field()	
