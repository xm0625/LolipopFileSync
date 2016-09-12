#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #
from project.exception.common_exception import CommonException
from project.core_server import core_server_helper as core_server_helper


def get_config(config_key):
    return core_server_helper.execute("getConfig", {"key": config_key})


def update_config(key, value):
    core_server_helper.execute("updateConfig", {"key": key, "value": value})


def save_config():
    core_server_helper.execute("saveConfig", {})
