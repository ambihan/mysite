#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/9/2 22:15
# @Author: haoxiang

"""
serializers.py
~~~~~~~~~~~~~~~~

"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'created_time',
            'excerpt',
            'category',
            'author',
            'views',
        ]
