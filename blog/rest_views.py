#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/9/2 21:51
# @Author: haoxiang

"""
rest_views.py
~~~~~~~~~~~~~~~~

"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import *


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    serializer_class_table = {
        'list': PostListSerializer,
        'retrieve': PostRetrieveSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class_table.get(
            self.action, super().get_serializer_class()
        )
