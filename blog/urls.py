#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/8/21 22:39
# @Author: haoxiang

"""
urls.py
~~~~~~~~~~~~~~~~

"""

from django.urls import path, include
from rest_framework import routers
from comments.rest_views import CommentViewSet
from . import views, rest_views
from .feeds import AllPostsRssFeed

app_name = 'blog'
router = routers.DefaultRouter()
router.register(r'posts', rest_views.PostViewSet, basename='post')
router.register(r'categories', rest_views.CategoryViewSet, basename='category')
router.register(r'tags', rest_views.TagViewSet, basename='tag')
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/', views.PostView.as_view(), name='posts'),
    path('archive/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('all/rss/', AllPostsRssFeed(), name='rss'),
    path('search/', views.search, name='search'),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
