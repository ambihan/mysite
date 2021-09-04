#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/9/2 22:15
# @Author: haoxiang

"""
serializers.py
~~~~~~~~~~~~~~~~

"""
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "name",
            "email",
            "url",
            "text",
            "created_time",
            "post",
        ]
        read_only_fields = [
            "created_time",
        ]
        extra_kwargs = {"post": {"write_only": True}}
