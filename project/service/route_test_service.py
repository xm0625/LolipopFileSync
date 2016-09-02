#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #
from project.exception.common_exception import CommonException
from project.sqlite_manager import sqlite_manager_client_helper as helper
import socket


def get_greeting_words(username):
    if username is None:
        raise CommonException("0", "username is empty!")
    return "hello, " + username


def get_all_books():
    sqlite_manager = helper.SqliteManager(address=('127.0.0.1', 50001), authkey='123456')
    try:
        sqlite_manager.connect()
    except socket.error as _:
        raise CommonException("0", "服务连接超时")

    result = helper.execute_batch(sqlite_manager, [
        {"method": helper.ExecuteSqlMethod.execute, "sql": "select * from book;", "param": []}],
                                  helper.ExecuteSqlResultMethod.fetchall, timeout=2)
    return result


def add_books(title, author, published):
    sqlite_manager = helper.SqliteManager(address=('127.0.0.1', 50001), authkey='123456')
    try:
        sqlite_manager.connect()
    except socket.error as _:
        raise CommonException("0", "服务连接超时")

    helper.execute_batch(sqlite_manager, [
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [title, author, published]}],
                         helper.ExecuteSqlResultMethod.rowcount, timeout=2)
    return