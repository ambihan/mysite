#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date:   2021/8/28 16:07
# @Author: haoxiang

"""
fabfile.py
~~~~~~~~~~~~~~~~

"""

from fabric import task, Connection

from invoke import Responder
from _credentials import *


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    # 远端服务器连接创建
    remote = Connection('%s@%s' % (ssh_username, ssh_host), connect_kwargs={"password": ssh_password})
    project_root_path = '~/apps/mysite/'

    # 进入项目根目录
    with remote.cd(project_root_path):
        # 先停止应用
        cmd = 'docker-compose -f production.yml stop'
        remote.run(cmd)

        # 从Git拉取最新代码
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        remote.run(cmd, watchers=responders)

        # 重新启动应用
        cmd = 'docker-compose -f production.yml up -d'
        remote.run(cmd)
