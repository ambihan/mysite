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
    path('', views.IndexView.as_view(), name='index'),
    path('posts', views.PostView.as_view(), name='posts'),
    path('archive/<int:year>/<int:month>', views.ArchiveView.as_view(), name='archive'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
]
