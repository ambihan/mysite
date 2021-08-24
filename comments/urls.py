#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date:   2021/8/24 14:54
# @Author: haoxiang

"""
urls
~~~~~~~~~~~~~~~~

"""

from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
]
