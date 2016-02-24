# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views import generic
from .models import tencent_article,tencent_comment,sina_article,sina_comment,sohu_article,sohu_comment


# Create your views here.
class NewsListView(generic.ListView):
    template_name = 'news_opin/index.html'
    context_object_name = 'hot_news_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return [tencent_article.objects.order_by('-time')[:100],sina_article.objects.order_by('-put_time')[:100],sohu_article.objects.order_by('-put_time')[:100]]

