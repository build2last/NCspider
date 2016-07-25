 # -*- coding:utf-8 -*-
import datetime
import time
from django.shortcuts import render
from django.views import generic
from .models import tencent_article,tencent_comment,sina_article,sina_comment,sohu_article,sohu_comment
from django.http import HttpResponse,Http404
from snownlp import SnowNLP as nlp

def show(request):
    delta=datetime.timedelta(days=2)#展示日期区间
    hot_sina_news=sina_article.objects.filter(put_time__gte=datetime.date.today()-delta).exclude(title__isnull=True).exclude(title__exact='').order_by('-comments_number')[:20]
    hot_tencent_news=tencent_article.objects.filter(put_time__gte=datetime.date.today()-delta).exclude(title__isnull=True).exclude(title__exact='').order_by('-comments_number')[:20]
    hot_sohu_news=sohu_article.objects.filter(put_time__gte=datetime.date.today()-delta).exclude(title__isnull=True).exclude(title__exact='').order_by('-comments_number')[:20]
    return render(request, 'news_opin/hot_news.html',
      {
            'hot_sina_news': hot_sina_news,
            'hot_tencent_news':hot_tencent_news,
            'hot_sohu_news':hot_sohu_news,
      }
)



def sina_cmt(request,comment_id):
    comment_id='comos-'+comment_id
    lastern_comments=sina_comment.objects.filter(news_id=comment_id).order_by('-put_time')[:50]
    attitude_tendency = []
    for com in lastern_comments:
        s = nlp(com.comment)
        senti_number = s.sentiments
        attitude_tendency.append(senti_number)
        rgb_list = ["#565D8E", "#499AA1","#FFFFFF", "#F9E063", "#BBDC37"]
        rgb_level = 2
        if senti_number  > 0.7 and senti_number <0.8:
            rgb_level = 3
        elif senti_number >=0.8:
            rgb_level = 4
        elif senti_number < 0.35 and senti_number > 0.25:
            rgb_level = 1
        elif senti_number <= 0.25:
            rgb_level = 0
        #senti_rgb = str(hex(int( senti_number * 0xFFFFFF))).replace("0x", "#").upper()
        senti_rgb = rgb_list[rgb_level]
        com.sense_color = senti_rgb
    tendency_number = sum(attitude_tendency)/len(attitude_tendency)
    attitude_list = ["很消极", "消极", "中立", "积极", "很积极"]
    attitude = attitude_list[ int(round(tendency_number*10/2)) -1 ]
    #return HttpResponse(comment_id)#str(sina_comment.objects.filter(news_id=comment_id).values("username")))    
    return render(request, 'news_opin/sina_comment_list.html',
           {
             'comments_list':lastern_comments,
             'attitude':attitude + '?',
           }  
          )

def sohu_cmt(request,comment_id):
    #return HttpResponse(str(sohu_comment.objects.filter(news_id=comment_id).values("author")))#留作DEBUG用
    lastern_comments=sohu_comment.objects.filter(news_id=comment_id)[:50]
    attitude_tendency = []
    for com in lastern_comments:
        s = nlp(com.comment)
        senti_number = s.sentiments
        attitude_tendency.append(senti_number)
        rgb_list = ["#565D8E", "#499AA1","#FFFFFF", "#F9E063", "#BBDC37"]
        rgb_level = 2
        if senti_number  > 0.7 and senti_number <0.8:
            rgb_level = 3
        elif senti_number >=0.8:
            rgb_level = 4
        elif senti_number < 0.35 and senti_number > 0.25:
            rgb_level = 1
        elif senti_number <= 0.25:
            rgb_level = 0
        #senti_rgb = str(hex(int( senti_number * 0xFFFFFF))).replace("0x", "#").upper()
        senti_rgb = rgb_list[rgb_level]
        com.sense_color = senti_rgb
    tendency_number = sum(attitude_tendency)/len(attitude_tendency)
    attitude_list = ["很消极", "消极", "中立", "积极", "很积极"]
    attitude = attitude_list[ int(round(tendency_number*10/2)) -1 ]
    return render(request, 'news_opin/sohu_comment_list.html',
           {
             'sohu_comments_list':lastern_comments,
             'attitude':attitude + "?",
           }  
          )




