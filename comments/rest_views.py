#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/9/4 18:34
# @Author: haoxiang

"""
rest_views.py
~~~~~~~~~~~~~~~~

"""
from rest_framework import mixins, viewsets
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
