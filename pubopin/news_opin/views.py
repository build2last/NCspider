 # -*- coding:utf-8 -*-
import datetime
import time
from django.shortcuts import render
from django.views import generic
from .models import tencent_article,tencent_comment,sina_article,sina_comment,sohu_article,sohu_comment
from django.http import HttpResponse,Http404

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
    #return HttpResponse(comment_id)#str(sina_comment.objects.filter(news_id=comment_id).values("username")))    
    return render(request, 'news_opin/sina_comment_list.html',
           {
             'comments_list':lastern_comments,
           }  
          )

def sohu_cmt(request,comment_id):
    #return HttpResponse(str(sohu_comment.objects.filter(news_id=comment_id).values("author")))#留作DEBUG用
    lastern_comments=sohu_comment.objects.filter(news_id=comment_id)[:50]
    return render(request, 'news_opin/sohu_comment_list.html',
           {
             'sohu_comments_list':lastern_comments,
           }  
          )




