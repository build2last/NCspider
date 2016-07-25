#-*- coding:utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from . import views

urlpatterns = [
	url(r'^$',views.show),
    url(r'^comment/sohu/cmt/$',views.sohu_cmt),
    url(r'^comment/sina/cmt/$',views.sina_cmt),
]
