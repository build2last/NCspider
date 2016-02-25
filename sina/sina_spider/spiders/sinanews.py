# -*- coding:utf-8 -*-
"""
#author: liu-kun
#Email: lancelotdev@163.com
#输出数据已经全部转为UTF-8，待完善：对花边(图片)新闻 & 视频新闻的处理
#-----说明-----：
1.[INFO]接口返回的网友互动量信息如下，我采用total反应热度，但是获取的评论数量为“show”少于总数量
"count": {
"qreply": 17313,
"total": 19392,
"show": 288
}
date:2016-02-18
author:liu-kun
2.[INFO]一些新闻内容未做处理
彩票信息 http://sports.sina.com.cn/l/2016-02-24/doc-ifxprucs6460405.shtml
体育视频 http://sports.sina.com.cn/uclvideo/bn/2016-02-24/050565188721.html
date:2016-02-25
author:liu-kun
--------------
"""
import urllib2
import re
import datetime
import json
import time
import scrapy
from urlparse import urlparse
from sina_spider.items import SimpleNews,NewsItem,commentItem
from scrapy.http import Request
import logging


logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
			datefmt='%a, %d %b %Y %H:%M:%S',
			filename='scrapy.log',
			filemode='w')


class newsSpider(scrapy.Spider):
	name = "sina"
	allowed_domains = ["sina.com.cn"]
	delta=datetime.timedelta(days=1) 
	yesterday=str((datetime.datetime.now()-delta).strftime("20%y-%m-%d"))
	news_date=yesterday#设定抓取新闻日期
	start_urls = [
		"http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&date="
		+news_date+"&ch=01&k=&offset_page=0&offset_num=0&num=5000&asc=&page="
		]


	def __init__(self):
		delta=datetime.timedelta(days=1) 
		yesterday=str((datetime.datetime.now()-delta).strftime("20%y-%m-%d"))
		news_date=yesterday#设定抓取新闻日期
		

	def parse(self, response):
		if  response.url.startswith("http://roll.news.sina.com.cn/"):
			try:
					response_html=response.body		 
					newsDic=json.loads(self.sina_api_process(response_html),strict=False)	   
					for i in range(0,len(newsDic["list"])):
						news_url=newsDic["list"][i]["url"] 
						if news_url.startswith("http://video") or news_url.startswith("http://slide"):
							continue							
						item = SimpleNews()#item
						item["flag"]="simplenews"
						item['title'] =newsDic["list"][i]["title"].encode("utf-8")
						item['newsUrl'] =news_url.encode("utf-8")
						item['source'] ="sina"
						item['category']=newsDic["list"][i]["channel"]["title"].encode("utf-8")
						temp_date= datetime.datetime.utcfromtimestamp(newsDic["list"][i]["time"])#日期章格式转换
						item['put_time']=temp_date.strftime('%Y-%m-%d %H:%M:%S')
						yield Request(url=newsDic["list"][i]["url"], callback=self.parse)
						yield item
			except Exception as ex :	
				logging.error("error0:Parse ERROR"+str(ex))				
		
		elif (not response.url.startswith("http://roll.news.sina.com.cn/")) and "comment5" not in response.url:	
			item=NewsItem()#item
			temp=response.xpath('//meta[contains(@name,"comment")]/@content').extract_first()
			temp=self.str_decode(temp)
			two_words=temp.split(":")
			item["newsUrl"]=response.url
			item['news_ID']=two_words[1].strip("comos-").encode("utf-8")
			comment_url="http://comment5.news.sina.com.cn/page/info?format=json&channel="+two_words[0]+"&newsid="+two_words[1]+"&page_size=200"
			item['comment_url']=comment_url.encode("utf-8")
			html_list=response.xpath("//div[@id='artibody']//p/text()").extract()
			news_content=''
			for i in html_list:
				news_content=news_content+i
			item['news_body']=news_content.encode("utf-8")
			item['flag']="news_body"
			yield Request(url=comment_url,callback=self.parse)
			yield item

		elif "comment5" in response.url:
			commentHML=self.str_decode(response.body)
			value = json.loads(commentHML,strict=False)	  
			try:
				news_item=NewsItem()#item
				news_item["comments_number"]=value["result"]["count"]["total"]
				news_item["flag"]="cmt number"			
				news_item["news_ID"]=value["result"]["news"]["newsid"].split('-')[-1].encode("utf-8")
				yield news_item
				cmlist=value["result"]["cmntlist"]
				item=commentItem()#item
				for i in range(len(cmlist)):
						item["flag"]="comment"		
						item["status"]=cmlist[i]["status"].encode("utf-8")
						item["usertype"]=cmlist[i]["usertype"].encode("utf-8")
						item["thread"]=cmlist[i]["thread"].encode("utf-8")
						item["parent"]=cmlist[i]["parent"].encode("utf-8")
						item["level"]=cmlist[i]["level"].encode("utf-8")
						item["ip"]=cmlist[i]["ip"].encode("utf-8")
						item["area"]=cmlist[i]["area"].encode("utf-8")
						item["newsid"]=cmlist[i]["newsid"].encode("utf-8")
						item["mid"]=cmlist[i]["mid"].encode("utf-8")
						item["against"]=cmlist[i]["against"].encode("utf-8")
						item["content"]=cmlist[i]["content"].encode("utf-8")
						item["nick"]=cmlist[i]["nick"].encode("utf-8")
						item["length"]=cmlist[i]["length"].encode("utf-8")
						item["rank"]=cmlist[i]["rank"].encode("utf-8")
						item["time"]=cmlist[i]["time"].encode("utf-8")
						item["vote"]=cmlist[i]["vote"].encode("utf-8")
						item["config"]=cmlist[i]["config"].encode("utf-8")
						item["agree"]=cmlist[i]["agree"].encode("utf-8")
						item["uid"]=cmlist[i]["uid"].encode("utf-8")
						item["newsUrl"]=response.url
						yield item
			except Exception as e:
				logging.error("error: comment_analyse:"+str(e))
				

	def sina_api_process(self,res):
		"""
		处理api 的response 返回的json,包括1.json数据说明 2.会引起错误的特殊字符
		"""
		try:
			data=res.decode("gbk").encode("utf-8")
			value=data[14:-1]
			value=value.replace("'s "," s ")
			keylist=["serverSeconds","last_time","path","title","cType","count","offset_page","offset_num","list","channel","url","type","pic"]
			#关键字+ 空格作为识别键值关键字的格式
			for i in keylist:            
				value=value.replace(i+" ","\""+i+"\"")
			value=value.replace("time :","\"time\":")
			value=value.replace("id :","\"id\":")	
			#去除会引起错误的 特殊字符
			badwords=["\b"]        
			for i in badwords:
				value=value.replace(i,"")
			value=value.replace("'", "\"") 
			return value
		except Exception as ex :	
			logging.error("error  1:Parse ERROR"+str(ex))


	def str_decode(self,tHTML):
		"""
		HTML解码
		:param: url
		:return: decoded html
		"""
		data=tHTML
		charset=re.findall('encoding.*?"(\w+)"',data)
		if len(charset)>0:
			data=data.decode(charset[0])
		if "gbk" in data:
			data=data.decode("gbk")
		return data

