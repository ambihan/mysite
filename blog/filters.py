#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/9/4 17:38
# @Author: haoxiang

"""
filters.py
~~~~~~~~~~~~~~~~

"""

from django_filters.rest_framework import FilterSet, NumberFilter
from .models import Post


class PostFilter(FilterSet):
    created_year = NumberFilter(
        field_name="created_time", lookup_expr="year"
    )
    created_month = NumberFilter(
        field_name="created_time", lookup_expr="month"
    )

    class Meta:
        model = Post
        fields = ["category", "tags", "created_year", "created_month"]
