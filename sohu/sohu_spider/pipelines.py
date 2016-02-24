# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi 

logging.basicConfig(
	level=logging.WARNING,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='sohu_spider.log',
	filemode='w')


class SohuPipeline(object):
    """
    twisted.enterprise.adbapi: Twisted RDBMS support.
    https://twistedmatrix.com/documents/14.0.0/core/howto/rdbms.html
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.dbpool.runQuery("""create table if not exists news_opin_sohu_article(
               news_id varchar(50) not null,
                primary key(news_id),
               title varchar(200),   
                time datetime,
                comments_number int,
                content text
                )charset='utf8'""")
        self.dbpool.runQuery("""create table if not exists news_opin_sohu_comment(     
                news_id varchar(50) not null,
		primary key(news_id),
                comments_id varchar(50),   
                author varchar(50),           
                datetime varchar(100),
                comment text
                )charset='utf8'""")

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        kw = dict(
            host=settings.get('MYSQL_HOST',' localhost'),
            port=settings.get('MYSQL_PORT', 3306),
            user=settings.get('MYSQL_USER', 'root'),
            db=settings.get('MYSQL_DB', 'sohu'),
            passwd=settings.get('MYSQL_PASSWD', ''),
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **kw)
        return cls(dbpool)


    def process_item(self, item, spider):
        """过滤无效项目,调试期间建议注释掉"""
        if not item.get('news_id'):
                raise DropItem("Missing news_id in %s" % item)
		"""============================="""
        d = self.dbpool.runInteraction(self._do_execute, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d


    def _do_execute(self, conn, item, spider):
 	"""
        conn.runQuery() <--> cursor.execute(), return cursor.fetchall();
        conn.execute(), then result = conn.fetchall()
        """
        if item['flag'] == 'article':
            if conn.execute("select 1 from  news_opin_sohu_article where news_id=%s", (item['news_id'],)):
                if not item['content']:
                    try:
                        conn.execute(
                            """update news_opin_sohu_article set title=%s, put_time=%s, comments_number=%s, news_url=%s
                           where news_id=%s""",
                            (
                                 item['title'], item['time'], item['comments_number'],item['news_id'],item['news_url']
                            )
                        )
                    except Exception as e:
                        logging.error(str(e))
                else:
                    conn.execute(
                        """update news_opin_sohu_article set content=%s where news_id=%s""",
                        (item['content'], item['news_id'])
                    )
            else:
                try:
                        conn.execute(
                                """insert into news_opin_sohu_article (news_id,comments_number,title,put_time,content,news_url)
                                values (%s,%s,%s,%s,%s,%s)""",
                                (
                                    item['news_id'],item['comments_number'],item['title'],item['time'],'',item['news_url'])
                        )
                except Exception as e:
                        logging.error("insert article exception "+str(e))
                        conn.execute(
                        """insert into news_opin_sohu_article (news_id,comments_number)
                        values (%s,%s)""",
                        (
                            item['news_id'],item['comments_number'])
                )

        elif item['flag'] == 'comment':
            
              conn.execute(
                        """insert into  news_opin_sohu_comment (news_id, comments_id, datetime, comment, author) values (%s, %s, %s, %s, %s)""",
                        (
                            item['news_id'], item['comments_id'], item['datetime'], item['comment'],
                            item['author']
                        )
                )


    def _handle_error(self, failure, item, spider):
        logging.error(str(failure))
