﻿# NCspider  项目简介   
##中文门户网站新闻和评论抓取。

###开发目的
    获取门户网站原始新闻及评论素材，结构化存储后为分析新闻舆情提供数据基础。 
    门户网站新闻有着微博不可替代的一些特点。 

###Written in [python], powered by [scrapy]. 
请参考配置说明，为了方便展示，可以结合django建立数据库

只需要爬虫的话建立database后修改settings.py相应参数就好了

对于网页的解析只用了re正则解析

爬虫可以单独使用，暂时只提供mysql支持
##简单介绍
* 包括新浪新闻门户，腾讯新闻门户，搜狐新闻（移动端)**新闻**以及**评论**
* 独立为3个scarpy项目包
* 每日新闻数量上千，评论数量级数十万

##使用手册
  使用或再开发前请简单阅读一下源码中的注释便于使用

###配置运行环境---Way to insatll scrapy on ubuntu 
  1. sudo apt-get install libxml2-dev libxslt1-dev
  2. sudo apt-get install python-dev
  3. sudo apt-get install libssl-dev 
  4. sudo apt-get install libffi-dev
  5. pip install -r requirements.txt

###数据库使用
  1. 更改**settings.py**适应你的本地化，数据库的相关设置,或者在 pipeline中修改相关参数
  2. 做了一个匹配的Django models模型方便了解,查看[数据模型](https://github.com/build2last/NCspider/blob/master/pubopin/news_opin/models.py)

###All in one版本运行
  * /news$ scrapy allstart   即可运行所有爬虫
  * /news$ scrapy crawl sina
  * /news$ scrapy crawl tencent
  * /news$ scrapy crawl sohu

###配套系统
    python 2.7及标准库
    测试中使用Mysql数据库  
    Linux Ubuntu 14.04测试通过
    理论上跨平台

###一些python库的引用：
* Scrapy 1.0


##探过的坑：
1. 编码问题：
中文网页：对中文的解析需要特别注意编码问题，utf-8是多数，但有时网站会采用GBK,GBK2312等编码格式。
数据库编码：出现了一大堆乱七八糟的文字，可以怀疑数据库字段编码跟内容编码不一致。
2. 利用django建立数据库时会有一些被默认的参数可能会被忽略，比如说数据项默认为非空 not null = true,所以说：使用前请认真阅读document

###In the future：
* 内容更全面，有更棒的接口请联系我
* 结构更合理
* 运行更高效
* scrapy是一个优秀的爬虫框架，结构合理，提供多线程，以后随着学习的深入会试着将更多成果运用进来。
* Long time supported.


##声明
* Email：**lancelotdev@163.com**
* Author：liu kun
* Last-Modified：2016-05

### To do list:
 * HTML cache: cause the slow query of the huge data.

[python]:https://www.python.org/
[scrapy]:http://scrapy.org/
