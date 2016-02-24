# coding:utf-8
from django.db import models

# Create your models here.
class tencent_article(models.Model):
	"""11 elements"""
	class Meta:
		ordering=['-time']
		verbose_name="标题"
	news_id = models.CharField(max_length=50)
	parent_name = models.CharField(max_length=200)#unique for tencent eg:news_news_top
	news_url = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	abstract = models.CharField(max_length=200)
	source = models.CharField(max_length=50)
	time = models.DateTimeField(u'')
	content = models.TextField()
	comments_id = models.CharField(max_length=60)
	comments_url = models.CharField(max_length=200)
	comments_number = models.IntegerField(default=0)

class tencent_comment(models.Model):
	#news=models.ForeignKey(tencent_article,verbose_name="tecent related news")
	news_id =models.CharField(max_length=50)
	comments_id = models.CharField(max_length=50)
	username = models.CharField(max_length=100)
	comment = models.TextField()
	put_time = models.DateTimeField()
	sex = models.CharField(max_length=10)
	reply_id = models.CharField(max_length=50)
	agree_count = models.IntegerField(default=0)


class  sina_article(models.Model):
	news_id=models.CharField(max_length=100)
	title = models.CharField(max_length=200)
	news_url = models.CharField(max_length=200)
	source=models.CharField(max_length=50)
	category=models.CharField(max_length=50)
	put_time=models.DateTimeField()
	content=models.TextField()
	comment_url=models.CharField(max_length=250)
	comments_number = models.IntegerField(default=0)

class sina_comment(models.Model):
	news_id =models.CharField(max_length=100)
	m_id = models.CharField(unique=True,max_length=50)
	username = models.CharField(max_length=100)
	comment = models.TextField()
	put_time = models.DateTimeField()
	#sex = models.CharField(max_length=10)
	parent_id = models.CharField(max_length=50)
	agree_count = models.IntegerField(default=0)
	against_count=models.IntegerField()


class sohu_article(models.Model):
	news_id=models.CharField(primary_key=True,max_length=100)
	title=models.CharField(max_length=300)
	put_time=models.DateTimeField()
	comments_number=models.IntegerField()
	content=models.TextField()
	news_url=models.CharField(max_length=200)

class sohu_comment(models.Model):
	news=models.ForeignKey(sohu_article,verbose_name="sohu related news")
	#news_id=models.CharField(max_length=100)
	comments_id=models.CharField(max_length=100)
	author=models.CharField(max_length=50)
	datetime=models.DateTimeField()
	comment=models.TextField()


