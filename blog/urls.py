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
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archive/<int:year>/<int:month>', views.archive, name='archive'),
    path('category/<int:pk>/', views.category, name='category'),
    path('tag/<int:pk>/', views.tag, name='tag'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('posts', views.posts, name='posts'),
]
