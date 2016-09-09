#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #
import os

def get_path_create_time(path):
    second = 0
    try:
        second = os.path.getctime(path)
    except os.error as _:
        pass
    millisecond = long(second * 1000)
    return millisecond


def get_path_modify_time(path):
    second = 0
    try:
        second = os.path.getmtime(path)
    except os.error as _:
        pass
    millisecond = long(second * 1000)
    return millisecond


def get_path_access_time(path):
    second = 0
    try:
        second = os.path.getatime(path)
    except os.error as _:
        pass
    millisecond = long(second * 1000)
    return millisecond


def get_path_size(path):
    size = 0
    try:
        size = os.path.getsize(path)
    except os.error as _:
        pass
    return size


def list_root_dir():
    result_list = []
    all_item_list = []
    if sys.platform == "win32":
        all_item_list = _list_windows_root_dir()
    elif os.path.isdir("/"):
        all_item_list = os.listdir("/")
    else:
        return result_list
    all_item_list.sort()
    folder_list = []
    file_list = []
    target_path = "/"
    for item in all_item_list:
        if os.path.islink(item):
            continue
        if os.path.isdir(os.path.join(target_path, item)):
            folder_list += [item]
        else:
            file_list += [item]
    for folder in folder_list:
        full_path = os.path.join(target_path, folder)
        item_map = {
            "fullPath": full_path,
            "name": folder,
            "kind": "0",  # "0"为文件夹 "1"为文件(未确定类型) 其他为具体的文件类型
            "cTime": get_path_create_time(full_path),
            "aTime": get_path_access_time(full_path),
            "mTime": get_path_modify_time(full_path),
            "size": get_path_size(full_path)
        }
        result_list += [item_map]
    for fileName in file_list:
        full_path = os.path.join(target_path, fileName)
        item_map = {
            "fullPath": full_path,
            "name": fileName,
            "kind": "1",  # "0"为文件夹 "1"为文件(未确定类型) 其他为具体的文件类型
            "cTime": get_path_create_time(full_path),
            "aTime": get_path_access_time(full_path),
            "mTime": get_path_modify_time(full_path),
            "size": get_path_size(full_path)
        }
        result_list += [item_map]
    return result_list


def _list_windows_root_dir():
    all_item_list = []
    for i in xrange(65, 91):
        vol = chr(i) + ':'
        if os.path.isdir(vol):
            all_item_list += [vol+"\\"]
    return all_item_list


def list_dir(target_path):
    result_list = []
    all_item_list = os.listdir(target_path)
    all_item_list.sort()
    folder_list = []
    file_list = []
    for item in all_item_list:
        if os.path.islink(os.path.join(target_path, item)):
            continue
        if os.path.isdir(os.path.join(target_path, item)):
            folder_list += [item]
        else:
            file_list += [item]
    for folder in folder_list:
        full_path = os.path.join(target_path, folder)
        item_map = {
            "fullPath": full_path,
            "name": folder,
            "kind": "0",  # "0"为文件夹 "1"为文件(未确定类型) 其他为具体的文件类型
            "cTime": get_path_create_time(full_path),
            "aTime": get_path_access_time(full_path),
            "mTime": get_path_modify_time(full_path),
            "size": get_path_size(full_path)
        }
        result_list += [item_map]
    for fileName in file_list:
        full_path = os.path.join(target_path, fileName)
        item_map = {
            "fullPath": full_path,
            "name": fileName,
            "kind": "1",  # "0"为文件夹 "1"为文件(未确定类型) 其他为具体的文件类型
            "cTime": get_path_create_time(full_path),
            "aTime": get_path_access_time(full_path),
            "mTime": get_path_modify_time(full_path),
            "size": get_path_size(full_path)
        }
        result_list += [item_map]
    return result_list


if __name__ == "__main__":
    print(list_root_dir())
