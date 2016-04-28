#-*- coding:utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from . import views

urlpatterns = [
	url(r'^$',views.show),
    url(r'^comment/sohu/(?P<comment_id>.+)/$',views.sohu_cmt,name='comment_id'),
    url(r'^comment/sina/(?P<comment_id>.+)/$',views.sina_cmt,name='comment_id'),
]
