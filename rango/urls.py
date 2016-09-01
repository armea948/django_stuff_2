# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 14:40:12 2016

@author: Kimberly
"""

from django.conf.urls import url
from rango import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/', views.about, name='about'),
]
        