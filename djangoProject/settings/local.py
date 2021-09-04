#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date:   2021/8/27 11:39
# @Author: haoxiang

"""
local
~~~~~~~~~~~~~~~~

"""
from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a(f*&uwl)qgfhw1^=*c&bby#dnjgqs(1mwa%tzs=w_ywl133(n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
