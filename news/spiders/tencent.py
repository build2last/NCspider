# -*- coding: utf-8 -*-
#!/usr/bin python
"""
----Notice-----
1.[INFOR]可能以后会面临改动：*腾讯的新闻和相应评论通过comments_id相联系*，我也搞不清腾讯的API为什么要把article_id信息置空，因该是系统改动过的痕迹。
author：liu-kun
date：2016-02-19
2.[INFOR]视频内容无法抓取 eg:http://view.inews.qq.com/a/SSH2016022405333702  可以获取abstract字段内容
author：liu-kun
date：2016-02-24
---------------
"""
import re
import json
from datetime import datetime,timedelta
from scrapy import Spider, Request
from news.items import TencentArticle, TencentComment
import logging


logging.basicConfig(
	level=logging.WARNING,
	format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt = '%a, %d %b %Y %H:%M:%S',
	filename = 'tencent_spider.log',
	filemode = 'w')


class TencentSpider(Spider):
    name = "tencent"
    pipelines = ['TencentPipeline']
    allowed_domains = ["qq.com"]
    start_urls = (
            'http://r.inews.qq.com/getQQNewsIndexAndItems?uid=9224f71108b3a1f5&chlid=news_news_top', # 要闻
            'http://r.inews.qq.com/getQQNewsIndexAndItems?uid=9224f71108b3a1f5&chlid=news_news_js', # 江苏
            'http://r.inews.qq.com/getQQNewsIndexAndItems?uid=9224f71108b3a1f5&chlid=news_news_mil', # 军事
            'http://r.inews.qq.com/getQQNewsIndexAndItems?uid=9224f71108b3a1f5&chlid=news_news_ssh', # 社会
            'http://r.inews.qq.com/getQQNewsIndexAndItems?uid=9224f71108b3a1f5&chlid=news_news_ent', # 娱乐
            'http://r.inews.qq.com/getQQNewsIndexAndItems?uid=9224f71108b3a1f5&chlid=news_news_sports', # 体育
            'http://r.inews.qq.com/getQQNewsIndexAndItems?uid=9224f71108b3a1f5&chlid=news_news_istock', # 股票
            'http://r.inews.qq.com/getQQNewsIndexAndItems?uid=9224f71108b3a1f5&chlid=news_news_finance' # 财经
    )

    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")


    def parse(self, response):
        try:
            url = response.url.split('/')
            if url[3].startswith('getQQNewsIndex'):
                body = response.body
                body = json.loads(body)['idlist'][0]['ids']
                chlid = response.url.split('=')[-1]
                ids = []
                cnt = 0
                for it in body:
                    cnt += 1
                    ids.append(it['id'])
                    item = TencentArticle()
                    item['flag'] = 'article'
                    item['news_id'] = it['id']
                    item['comments_number'] = it['comments']
                    item['content'] = ''
                    yield item
                    if cnt % 20 == 0:
                        ids = ','.join(ids)
                        url = 'http://r.inews.qq.com/getQQNewsListItems?uid=9224f71108b3a1f5'\
                              + '&ids=' + ids + '&chlid=' + chlid
                        yield Request(url=url, callback=self.parse)
		        ids = []
            elif url[3].startswith('a'):#新闻内容页面处理  eg:http://view.inews.qq.com/a/NEW2016021001255109
                item = TencentArticle()
                item['flag'] = 'article'
                item['news_id'] = url[-1]
                try:
                    text_html= response.xpath('//div[@id="content"]').extract()[0]
                    r=re.compile("<.*?>",re.S)#除去html标签的正则表达  remove_compile
                    item['content'] = re.sub(r,'',text_html)
                except Exception as e:
                    logging.info("spider content debug正则匹配失败:" +str(e)+'   '+response.url)
                    item['content']="404"
                yield item
 #article eg:http://r.inews.qq.com/getQQNewsListItems?uid=9224f71108b3a1f5&ids=NEW2016021001255108&child=news_news_top
            elif url[3].startswith('getQQNewsList'):
                body = response.body 
                newslist = json.loads(body)['newslist']
                for news in newslist:
                    if not news['time'].startswith(self.date):#date为今日日期
                         continue
                    item = TencentArticle()
                    item['flag'] = 'article'
                    item['news_id'] = news['id']
                    item['parent_name'] = news['uinname']
                    item['url'] = news['url']
                    item['title'] = news['title']
                    item['abstract'] = news['abstract']
                    item['source'] = news['source']
                    item['time'] = news['time']
                    item['content'] = ''
                    item['comments_id'] = news['commentid']
                    tmp = news['url'].split('/')
                    tmp[3] = 'comment'
                    item['comments_url'] = '/'.join(tmp) + '#' + news['commentid']
                    item['comments_number'] = 0
                    yield item
                    url = 'http://view.inews.qq.com/a/' + item['news_id']
                    yield Request(url=url, callback=self.parse)
                    url = 'http://r.inews.qq.com/getQQNewsComment?uid=9224f71108b3a1f5&comment_id=%s&page=%s' \
                          % (item['comments_id'], 1)
                    yield Request(url=url, callback=self.parse)

    #comments eg:http://r.inews.qq.com/getQQNewsComment?uid=9224f71108b3a1f5&comment_id=1304296892&page=1
            elif url[3].startswith('getQQNewsComment'):
                body = response.body
                comments = json.loads(body)['comments']['new']
                if comments:
                    url = response.url.split('=')
                    url[-1] = str(int(url[-1]) + 1)
                    url = '='.join(url)
                    yield Request(url=url, callback=self.parse)
                for comment in comments:
                    for it in comment:
                        item = TencentComment()
                        item['flag'] = 'comment'
                        item['news_id'] = it['article_id']
                        item['comments_id'] = it['commentid']
                        item['username'] = it['mb_nick_name'] 
                        item['comment'] = it['reply_content']
                        item['datetime'] = datetime.fromtimestamp(int(it['pub_time'])).strftime('%Y-%m-%d %H:%M:%S')
                        item['sex'] = it['sex']
                        item['reply_id'] = it['reply_id']
                        item['agree_count'] = it['agree_count']
                        yield item
            
        except Exception as e:
            logging.error(str(e))