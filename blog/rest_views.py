#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/9/2 21:51
# @Author: haoxiang

"""
rest_views.py
~~~~~~~~~~~~~~~~

"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostListSerializer


@api_view(http_method_names=["GET"])
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    serializer = PostListSerializer(post_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
