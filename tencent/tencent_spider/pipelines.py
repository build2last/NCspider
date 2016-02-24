# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
 
logging.basicConfig(
	level=logging.WARNING,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='tencent_spider.log',
	filemode='w')


class TencentPipeline(object):
    """
    twisted.enterprise.adbapi: Twisted RDBMS support.
    https://twistedmatrix.com/documents/14.0.0/core/howto/rdbms.html
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool
		#self.dbpool.runQuery("""create table if not exists news_opin_tencent_article(
		#       news_id varchar(50) not null,
		#      primary key(news_id),
		#     news_url varchar(200),
		#    title varchar(200),
		#   abstract varchar(200),
		#  source varchar(50),
		# time datetime,
		#comments_url varchar(200),
		#       comments_id varchar(50),
		#      comments_number int,
		#     parent_name varchar(200),
		#    content text
		#   )charset='utf8'""")
		#self.dbpool.runQuery("""create table if not exists news_opin_tencent_comment(     
		#       news_id varchar(50) not null,
		#      comments_id varchar(50),
		#     sex char(10),
		#    username varchar(50),
		#   reply_id varchar(50),
		#  agree_count int,
		# put_time varchar(100),
		#comment text
		#)charset='utf8'""")

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        #数据库配置
        kw = dict(
            host=settings.get('MYSQL_HOST',' localhost'),
            port=settings.get('MYSQL_PORT', 3306),
            user=settings.get('MYSQL_USER', 'root'),
            db=settings.get('MYSQL_DB', 'tencent'),
            passwd=settings.get('MYSQL_PASSWD', '{{your pass words}}'),
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **kw)
        return cls(dbpool)

    def process_item(self, item, spider):
        """过滤无效项目,调试期间建议注释掉"""

        """============================="""
        d = self.dbpool.runInteraction(self._do_execute, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    def _do_execute(self, conn, item, spider):
        if item['flag'] == 'article':
            if conn.execute("select 1 from news_opin_tencent_article where news_id=%s", (item['news_id'],)):
                if not item['content']:
                    try:
                        conn.execute(
                            """update news_opin_tencent_article set news_url=%s, title=%s, abstract=%s, source=%s, parent_name=%s, time=%s,
                            comments_id=%s, comments_url=%s  where news_id=%s""",
                            (
                                item['url'], item['title'], item['abstract'], item['source'], item['parent_name'],
                                item['time'], item['comments_id'], item['comments_url'], item['news_id']
                            )
                        )
                    except Exception as e:
                        
                        conn.execute(
                            """update news_opin_tencent_article set comments_number=%s where news_id=%s""",
                            (item['comments_number'], item['news_id'])
                        )
                else:
                    conn.execute(
                        """update news_opin_tencent_article set content=%s where news_id=%s""",
                        (item['content'], item['news_id'])
                    )
            else:
                conn.execute(
                        """insert into news_opin_tencent_article (news_id, comments_number)
                        values (%s, %s)""",
                        (
                            item['news_id'], item['comments_number']
                        )
                )

        elif item['flag'] == 'comment':
            if conn.execute("select 1 from news_opin_tencent_comment where reply_id=%s", (item['reply_id'], )):
                conn.execute(
                        """update news_opin_tencent_comment set agree_count=%s where reply_id=%s""",
                        (item['agree_count'], item['reply_id'])
                )
            else:
                conn.execute(
                        """insert into news_opin_tencent_comment (news_id, comments_id, put_time, comment, username, sex,
                        reply_id, agree_count) values (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            item['news_id'], item['comments_id'], item['datetime'], item['comment'],
                            item['username'], item['sex'], item['reply_id'], item['agree_count']
                        )
                )

    def _handle_error(self, failure, item, spider):
        logging.error(failure)
