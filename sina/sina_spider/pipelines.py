#-*- coding:utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from os import path
import logging
from scrapy import signals
import MySQLdb.cursors
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi

logging.basicConfig(
	level=logging.WARNING,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='scrapy.log',
	filemode='w')


class SinaNewsPipeline(object):
	def __init__(self,dbpool):
		self.dbpool = dbpool
		self.dbpool.runQuery("""create table IF NOT EXISTS news_opin_sina_article(
		news_id varchar(50) not null,
		primary key(news_id),
		news_url varchar(200),
		title varchar(200),
		source varchar(50),
		put_time datetime,
		comments_url varchar(250),
		category varchar(30),
		content text
		)""")
		
		self.dbpool.runQuery("""create table IF NOT EXISTS news_opin_sina_comment( 
			news_id varchar(50),    
			m_id varchar(50) not null,
			username varchar(60),
			comment text,
			put_time datetime,
			sex char(10),
			reply_id varchar(50),
			agree_count int,
			against_count int)""")	
	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		kw = dict(
			host=settings.get('MYSQL_HOST',' localhost'),
			port=settings.get('MYSQL_PORT', 3306),
			user=settings.get('MYSQL_USER', 'root'),
			db=settings.get('MYSQL_DB', 'pub_opinion'),
			passwd=settings.get('MYSQL_PASSWD', '{{your pass words}}'),
			charset='utf8',
			use_unicode=True,
		)
		dbpool = adbapi.ConnectionPool ('MySQLdb', **kw)
		return cls (dbpool)
	
	def process_item(self, item, spider):
		d = self.dbpool.runInteraction(self._do_execute, item, spider)
		d.addErrback(self._handle_error, item, spider)
		d.addBoth(lambda _: item)
		return d

	
	def _do_execute(self, conn, item, spider):
		"""
		conn.runQuery() <--> cursor.execute(), return cursor.fetchall();
		conn.execute(), then result = conn.fetchall()
		"""
		if item.get("flag")=="cmt number":
			try:
				conn.execute(
				         	"update news_opin_sina_article set comments_number=%s where news_id=%s",
				         	(item["comments_number"],item['news_ID'])
				     )
			except Exception as e:
				logging.error(str(e))
				    
		elif item.get('flag')=='simplenews':
			try:
				if conn.execute("select 1 from news_opin_sina_article where news_url =%s",(item['newsUrl'],)):
					conn.execute(
					         	"update news_opin_sina_article set title=%s, source=%s, category=%s, put_time=%s where news_url=%s",
					         	(item['title'] , item['source'],  item['category'],  item['put_time'],item['newsUrl'])
					     )
				else:
					conn.execute(
					         	"insert into news_opin_sina_article (news_url,title,source,category,put_time)  values (%s, %s,%s, %s,%s)",
					         	(item['newsUrl'] , item['title'] , item['source'],  item['category'],  item['put_time'])
					     )
			except Exception as ex :	
				logging.error("error:"+str(ex))
		elif item.get('flag')=="news_body":
			try:
					if not item['news_body']:
						try:
							conn.execute(
							         	"update news_opin_sina_article set content=%s, news_id=%s, comment_url=%s where news_url =%s",
							         	('',item['news_ID'],item['comment_url'],item['newsUrl'])
							     )
							logging.error("newsbody")###debug
						except :
							conn.execute(
							         	"update  news_opin_sina_article set content=%s, news_id=%s, comment_url=%s where news_url =%s",
							         	('', item[news_ID],'', item['newsUrl'])
							     )
					else:
						conn.execute(
							         	"update news_opin_sina_article set content=%s, news_id=%s, comment_url=%s where news_url =%s",
							         	(item['news_body'], item['news_ID'],item['comment_url'], item['newsUrl'])
							     )

			except Exception as ex :	
				logging.error("Error:"+str(ex))

		elif item.get("flag")=='comment':
			try:
				if conn.execute("select 1 from news_opin_sina_comment where m_id=%s",(item['mid'])):
					logging.info("one comment repeat: %s" % item)

				else:
					conn.execute(
							 "insert into  news_opin_sina_comment (news_id,  m_id,  username,  comment,  put_time,  parent_id,  agree_count,  against_count)  values (%s, %s,%s, %s,%s, %s,%s, %s)",
							 (	
							 	item["newsid"],	  item["mid"],  item["nick"],
							 	item["content"],  item["time"],item['parent'],
								item["agree"],item["against"],
							))
			except Exception as ex:	
				logging.error("insert comment error:"+str(ex))


	def _handle_error(self, failure, item, spider):
		logging.error(str(failure))
