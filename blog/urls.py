#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/8/21 22:39
# @Author: haoxiang

"""
urls.py
~~~~~~~~~~~~~~~~

"""

from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail')
]
