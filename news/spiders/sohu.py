# -*- coding: utf-8 -*-
#!/usr/bin python
"""
#说明：新闻api似乎在num=60时达到最多
#
#----------------Note Here-----------------
#1.The problem of the infomation's encoding has cause error and  I find it with about 5 hours.  
#So next time you process the Chinese doc you shall pay attention.
"""
import json
import re
from datetime import datetime,timedelta
from scrapy import Spider, Request
from news.items import SohuArticle, SohuComment
import logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='sohuscrapy.log',
    filemode='w')

class SohuSpider(Spider):
    name = "sohu"
    pipelines = ['SohuPipeline']
    allowed_domains = ["sohu.com"]
    start_urls = (
        'http://api.k.sohu.com/api/channel/v5/news.go?channelId=1&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=3&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=55&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=5&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=23&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=2&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=4&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=6&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=45&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=12&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=46&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=29&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=247&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=351&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=1159&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=185&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=275&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=97&num=60',
    'http://api.k.sohu.com/api/channel/v5/news.go?channelId=372&num=60'
    )
    def __init__(self):
        self.date = str(datetime.now().strftime('%Y-%m-%d'))#date constraint for Today
    def parse(self, response):
        url = response.url.split('/')
        if url[4].startswith('channel'):
            body = response.body
            articles = json.loads(body)['articles']            
            cnt = 0

            for it in articles: 
                try:
                    if (not it.get('time')) or (not it.get('title')):
                        continue
                    if not datetime.fromtimestamp(int( it.get('time'))/1000).strftime('%Y-%m-%d %H:%M:%S').startswith(self.date):
                       continue 
                    cnt += 1
                    item = SohuArticle()
                    item['flag'] = 'article'
                    item['news_id'] = it['newsId']
                    item['time']=datetime.fromtimestamp(int(it.get('updateTime'))/1000).strftime('%Y-%m-%d %H:%M:%S')
                    item['title']=it['title']
                    if  it.get('commentNum'):
                        item['comments_number'] = it.get('commentNum')
                    else:
                        item['comments_number'] = '0'
                    item['content'] = '' 
                    url = 'http://api.k.sohu.com/api/news/v4/article.go?newsId='+str(it['newsId'])
                    item['news_url']=url                    
                    yield item
                    yield Request(url=url, callback=self.parse)
                    comment_url = 'http://api.k.sohu.com/api/comment/getCommentListByCursor.go?busiCode=2&id=' +str(it['newsId'])
                    yield Request(url=comment_url, callback=self.parse)
                except Exception as e:
                        logging.error('spider'+str(e))
                    
                
        if url[4].startswith('comment'):
            body = response.body
            comments = json.loads(body,strict=False).get('response')
            if  comments:
                comments=comments['commentList']
                chlid = response.url.split('=')[-1]
                for it in comments:
                      item = SohuComment()
                      item['flag'] = 'comment'
                      item['news_id'] = chlid
                      item['comments_id'] = it['commentId']
                      item['author'] = it['author']
                      item['comment'] = it['content']
                      item['datetime'] =datetime.fromtimestamp(int(it['ctime'])/1000).strftime('%Y-%m-%d %H:%M:%S')
                      yield item
        if url[4].startswith('news'):
            chlid2 = response.url.split('=')[-1]
            item = SohuArticle()
            item['flag'] = 'article'
            item['news_id'] = chlid2
            try:
                original_html = response.xpath('/root/content').extract()[0]
                r=re.compile("&lt;p&gt;(.*?)&lt;/p&gt;")
                contents=re.findall(r,str(original_html.encode("utf-8")))
                content="".encode("utf-8")
                for i in contents:
                    content+=i
                item['content']=content
            except:
                item['content'] = 'no content'
            yield item      









