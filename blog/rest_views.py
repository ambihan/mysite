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
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor.bits import (
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    RetrieveSqlQueryKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

from comments.serializers import CommentSerializer
from .serializers import *
from .filters import PostFilter
from .utils import UpdatedAtKeyBit


class PostUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "post_updated_at"


class PostListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = PostUpdatedAtKeyBit()


class CommentUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "comment_updated_at"


class CommentListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = CommentUpdatedAtKeyBit()


class CategoryUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "category_updated_at"


class CategoryListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = CategoryUpdatedAtKeyBit()


class TagUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "tag_updated_at"


class TagListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = TagUpdatedAtKeyBit()


class PostObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = PostUpdatedAtKeyBit()


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

    @cache_response(timeout=5 * 60, key_func=CommentListKeyConstructor())
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

    @cache_response(timeout=5 * 60, key_func=PostListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(timeout=5 * 60, key_func=PostObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    permission_classes = [AllowAny]

    @cache_response(timeout=5 * 60, key_func=CategoryListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    permission_classes = [AllowAny]

    @cache_response(timeout=5 * 60, key_func=TagListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
