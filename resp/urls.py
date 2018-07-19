#coding:utf-8
'''
Created on 2016��10��28��

@author: ldl
'''
from django.conf.urls import url
from .views import callBack

urlpatterns = [
    # url(r'^',respBad),
    url(r'^callBack', callBack),
]