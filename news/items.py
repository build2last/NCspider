# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



#Get the basic information of a piece of news in the json from sina api.
class SimpleNews(scrapy.Item):
	title = scrapy.Field()#
	newsUrl = scrapy.Field()#
	source=scrapy.Field()#
	category=scrapy.Field()#
	put_time=scrapy.Field()#
	flag=scrapy.Field()

#Get the news body from the response html of news url. 
class NewsItem(scrapy.Item):
	newsUrl=scrapy.Field()
	news_body=scrapy.Field()#
	news_ID=scrapy.Field()#
	comment_url=scrapy.Field()#
	comments_number=scrapy.Field()
	flag=scrapy.Field()

class commentItem(scrapy.Item):
	status =scrapy.Field()
	usertype=scrapy.Field()
	thread=scrapy.Field()#本条评论回应的评论id   
	parent=scrapy.Field()#本条评论回应的评论id   
	level=scrapy.Field()
	ip=scrapy.Field()
	area=scrapy.Field()
	newsid=scrapy.Field()
	mid=scrapy.Field()
	against=scrapy.Field()
	content=scrapy.Field()
	nick=scrapy.Field()
	length=scrapy.Field()
	rank=scrapy.Field()
	time=scrapy.Field()
	vote=scrapy.Field()#？
	config=scrapy.Field()
	agree=scrapy.Field()
	uid=scrapy.Field()
	newsUrl=scrapy.Field()
	#sex=scrapy.Field()
	flag=scrapy.Field()


#---------sohu------------
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


#----------tencent--------
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

