# NCspider  项目简介   
## 中文门户网站新闻和评论抓取。
A Python Project

scrapy 中文编码处理 数据库配置 

### 编写目的
* 获取门户网站原始新闻及评论素材，结构化存储后，为分析舆情提供数据基础。 
* 门户网站新闻有着微博不可替代的一些特点。 
* 请参考配置说明，为了方便展示，可以结合django建立数据库
* 只需要爬虫的话建立database后修改settings.py相应参数就好了
* 对于网页的解析只用了re正则解析（快过Beautiful Soup）
* 爬虫 news 可以单独使用，暂时只提供mysql支持

## 简单介绍
* 包括新浪新闻门户，腾讯新闻门户，搜狐新闻（移动端)**新闻**以及**评论**
* 每日新闻数量上千，评论数量级数十万

### 从零开始配置运行环境---Way to insatll scrapy on ubuntu 
  1. sudo apt-get install libxml2-dev libxslt1-dev
  2. sudo apt-get install python-dev
  3. sudo apt-get install libssl-dev 
  4. sudo apt-get install libffi-dev
  5. pip install -r requirements.txt

### 数据库使用
  1. 更改**settings.py**适应你的本地化，数据库的相关设置,或者在 pipeline中修改相关参数
  2. 做了一个匹配的Django models模型方便了解,查看[数据模型](https://github.com/build2last/NCspider/blob/master/pubopin/news_opin/models.py)

### 使用命令
  * /news$ scrapy allstart   即可运行所有爬虫
  * /news$ scrapy crawl sina
  * /news$ scrapy crawl tencent
  * /news$ scrapy crawl sohu

### 配套系统
    python 2.7
    Mysql 
    Scrapy 1.0
    
### 测试
    Linux Ubuntu 14.04 tested
    Windows 10 tested

## 问题说明：
1. 编码问题：
  * 中文网页：对中文的解析需要特别注意编码问题，utf-8是多数，但有时网站会采用GBK,GBK2312等编码格式。
  * 数据库编码：出现了一大堆乱七八糟的文字，可以怀疑数据库字段编码跟内容编码不一致。
2. 利用django建立数据库时会有一些被默认的参数可能会被忽略，比如说数据项默认为非空 not null = true,所以说：使用前请认真阅读document


### 著作声明
* Email：**lancelotdev@163.com**
* Author：liu kun
* Last-Modified：2016-10

### To do list：
* 抓的更全
* code review，运行更高效
* scrapy是一个优秀的爬虫框架，结构合理，提供多线程，以后随着学习的深入会试着将更多成果运用进来。
* 支持更多数据库类型，包括 NoSQL
* HTML cache

### Journal

#### 2016-10-12
答辩完毕

[python]:https://www.python.org/
[scrapy]:http://scrapy.org/

### Update：
#### 2017-04-13
现在看来这个项目还是存在很多问题的：
1. 当初为了方便定制数据模型并于数据库同步，产生了 ORM(对象关系映射) 这个需求，碰巧用过 django 的那套东西，所以就直接拿来用了，现在知道有专门的工具 [SQLAlchemy](http://www.sqlalchemy.org/) 来解决这个问题了。
2. Mysql 数据量大之后进行查询真的好慢。
3. 文档的编写相当不专业。


