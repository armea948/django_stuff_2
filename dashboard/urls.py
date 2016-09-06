# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 14:55:07 2016

@author: Kimberly
"""

from django.conf.urls import url
from dashboard import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^forms$', views.get_name, name='forms'),
        url(r'^embed_api$', views.embed_api, name='embed_api'),
        #url(r'^report$', views.new_dateranges, name='report'),
]
        