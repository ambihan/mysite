#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/9/2 21:51
# @Author: haoxiang

"""
rest_views.py
~~~~~~~~~~~~~~~~

"""
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.serializers import DateField
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status

from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .filters import PostFilter
from comments.serializers import CommentSerializer


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    serializer_class_table = {
        'list': PostListSerializer,
        'retrieve': PostRetrieveSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class_table.get(
            self.action, super().get_serializer_class()
        )

    @action(methods=["GET"], detail=False, url_path="archive/dates", url_name="archive-date")
    def list_archive_dates(self, request, *args, **kwargs):
        dates = Post.objects.dates("created_time", "month", order="DESC")
        date_field = DateField()
        data = [date_field.to_representation(date) for date in dates]
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_path="comments",
        url_name="comment",
        pagination_class=LimitOffsetPagination,
        serializer_class=CommentSerializer,
    )
    def list_comments(self, request, *args, **kwargs):
        # 根据 URL 传入的参数值（文章 id）获取到博客文章记录
        post = self.get_object()
        # 获取文章下关联的全部评论
        queryset = post.comment_set.all().order_by("-created_time")
        # 对评论列表进行分页，根据 URL 传入的参数获取指定页的评论
        page = self.paginate_queryset(queryset)
        # 序列化评论
        serializer = self.get_serializer(page, many=True)
        # 返回分页后的评论列表
        return self.get_paginated_response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    permission_classes = [AllowAny]


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    permission_classes = [AllowAny]
