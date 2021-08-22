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

urlpatterns = [
    path('', views.index, name='index'),
]