#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #
from project.exception.common_exception import CommonException
from project.util import fs
from project.core_server import core_server_helper as core_server_helper
import socket

def list_dir(dir_id):
    fs_item_list = []
    if dir_id is None:
        fs_item_list = fs.list_root_dir()
    else:
        result = core_server_helper.execute("getPath",
                                            {"id": str(dir_id)})
        fs_item_list = fs.list_dir(result)
    start_id = core_server_helper.execute("getStartId",
                                        {"idNum": len(fs_item_list)})
    dict_obj = {}
    for item in fs_item_list:
        item["id"] = start_id
        dict_obj[str(start_id)] = item["fullPath"]
        start_id += 1
        if item["kind"] == "0":
            item["state"] = "closed"
        else:
            item["state"] = "open"
    result = core_server_helper.execute("putIdPathMap",
                                        dict_obj)
    return fs_item_list


def reload_dir():
    result = core_server_helper.execute("reloadDir", None)
    return None