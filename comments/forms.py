#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date:   2021/8/24 14:09
# @Author: haoxiang

"""
forms
~~~~~~~~~~~~~~~~

"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
