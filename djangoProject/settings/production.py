#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date:   2021/8/27 11:40
# @Author: haoxiang

"""
production
~~~~~~~~~~~~~~~~

"""
from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.smoba.cn']

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis://:UJaoRZlNrH40BDaWU6fi@redis:6379/0",
        "OPTIONS": {
            "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            "CONNECTION_POOL_CLASS_KWARGS": {"max_connections": 50, "timeout": 20},
            "MAX_CONNECTIONS": 1000,
            "PICKLE_VERSION": -1,
        },
    },
}
