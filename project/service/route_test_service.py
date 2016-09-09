#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #
from project.exception.common_exception import CommonException
from project.sqlite_manager import sqlite_server_helper as helper


def get_greeting_words(username):
    if username is None:
        raise CommonException("0", "username is empty!")
    return "hello, " + username


def get_all_books():
    result = helper.execute_batch([
        {"method": helper.ExecuteSqlMethod.execute, "sql": "select * from book;", "param": []}],
                                  helper.ExecuteSqlResultMethod.fetchall)
    return result


def add_books(title, author, published):
    helper.execute_batch([
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [title, author, published]}],
                         helper.ExecuteSqlResultMethod.rowcount)
    return