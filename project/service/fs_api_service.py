#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 解决py2.7中文出现write错误的问题
import os
import sys

from project.util.byteify import byteify

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #
from project.exception.common_exception import CommonException
from project.util import fs
from project.core_server import core_server_helper as core_server_helper
from project.util.md5_sum import md5sum


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
            item.pop("size")
        else:
            item["state"] = "open"
    result = core_server_helper.execute("putIdPathMap",
                                        dict_obj)
    return fs_item_list


def reload_dir():
    result = core_server_helper.execute("reloadDir", None)
    return None


def walk_and_gen_path_info(target_folder):
    if not target_folder.endswith(os.path.sep):
        target_folder += os.path.sep
    data = {"dirs": [], "files": {}}
    for root, dirs, files in os.walk(target_folder):
        for dir_name in dirs:
            full_name = os.path.join(root, dir_name)
            if os.path.islink(full_name):
                continue
            if root == target_folder:
                relative_name = dir_name
            else:
                relative_name = os.path.join(root[len(target_folder):999999], dir_name)
            relative_name = relative_name.replace(os.path.sep, "/")
            data["dirs"] += [relative_name]
        for file_name in files:
            full_name = os.path.join(root, file_name)
            if os.path.islink(full_name):
                continue
            md5_sum = ""
            try:
                md5_sum = md5sum(full_name)
            except IOError as _:
                pass
            if root == target_folder:
                relative_name = file_name
            else:
                relative_name = os.path.join(root[len(target_folder):999999], file_name)
            relative_name = relative_name.replace(os.path.sep, "/")
            data["files"][relative_name] = md5_sum
    return byteify(data)


def diff_path_info(src_path_info, dst_path_info):
    result = {"src_not_exist": {"dirs": [], "files": []}, "dst_not_exist": {"dirs": [], "files": []},
              "src_dst_diff_files": []}
    src_dirs_set = set(src_path_info["dirs"])
    dst_dirs_set = set(dst_path_info["dirs"])
    src_files_set = set(src_path_info["files"].keys())
    dst_files_set = set(dst_path_info["files"].keys())
    src_not_exist_dirs = list(dst_dirs_set - src_dirs_set)
    dst_not_exist_dirs = list(src_dirs_set - dst_dirs_set)
    src_not_exist_files = list(dst_files_set - src_files_set)
    dst_not_exist_files = list(src_files_set - dst_files_set)
    src_dst_exist = src_files_set & dst_files_set
    src_dst_diff_files = []
    for file_key in src_dst_exist:
        if src_path_info["files"][file_key] != dst_path_info["files"][file_key]:
            src_dst_diff_files += [file_key]
    result["src_not_exist"]["dirs"] = src_not_exist_dirs
    result["src_not_exist"]["files"] = src_not_exist_files
    result["dst_not_exist"]["dirs"] = dst_not_exist_dirs
    result["dst_not_exist"]["files"] = dst_not_exist_files
    result["src_dst_diff_files"] = src_dst_diff_files
    return result
