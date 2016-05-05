# coding:utf-8
from django.db import models

# Create your models here.
class tencent_article(models.Model):
	"""11 elements"""
	class Meta:
		ordering=['-put_time']
		verbose_name="腾讯"
	news_id = models.CharField(max_length=100, null=True)
	parent_name = models.CharField(max_length=200, null=True)#unique for tencent eg:news_news_top
	news_url = models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=200, null=True)
	abstract = models.CharField(max_length=200, null=True)
	source = models.CharField(max_length=50, null=True)
	put_time = models.DateTimeField(u'', null=True)
	content = models.TextField()
	comments_id = models.CharField(max_length=100, null=True)
	comments_url = models.CharField(max_length=200, null=True)
	comments_number = models.IntegerField(default=0)

class tencent_comment(models.Model):
	#news=models.ForeignKey(tencent_article,verbose_name="tecent related news")
	news_id =models.CharField(max_length=200, null=True)
	comments_id = models.CharField(max_length=200, null=True)
	username = models.CharField(max_length=200, null=True)
	comment = models.TextField(null=True)
	put_time = models.DateTimeField(null=True)
	sex = models.CharField(max_length=10,null=True)
	reply_id = models.CharField(max_length=200, null=True)
	agree_count = models.IntegerField(default=0,null=True)


class  sina_article(models.Model):
	news_id=models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=200, null=True)
	news_url = models.CharField(max_length=200, null=True)
	source=models.CharField(max_length=50, null=True)
	category=models.CharField(max_length=50, null=True)
	put_time=models.DateTimeField(null=True)
	content=models.TextField(null=True)
	comments_url=models.CharField(max_length=250, null=True)
	comments_number = models.IntegerField(default=0, null=True)

class sina_comment(models.Model):
	news_id =models.CharField(max_length=200, null=True)
	m_id = models.CharField(unique=True,max_length=200)
	username = models.CharField(max_length=100, null=True)
	comment = models.TextField(null=True)
	put_time = models.DateTimeField(null=True)
	#sex = models.CharField(max_length=10)
	parent_id = models.CharField(max_length=200, null=True)
	agree_count = models.IntegerField(default=0, null=True)
	against_count=models.IntegerField(null=True)


class sohu_article(models.Model):
	news_id=models.CharField(primary_key=True,max_length=150)
	title=models.CharField(max_length=300, null=True)
	put_time=models.DateTimeField(null=True)
	comments_number=models.IntegerField(null=True)
	content=models.TextField(null=True)
	news_url=models.CharField(max_length=200,null=True)

class sohu_comment(models.Model):
	news=models.ForeignKey(sohu_article,verbose_name="sohu related news")
	comments_id=models.CharField(max_length=200, null=True)
	author=models.CharField(max_length=50, null=True)
	datetime=models.DateTimeField(null=True)
	comment=models.TextField(null=True)