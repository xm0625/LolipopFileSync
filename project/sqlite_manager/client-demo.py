# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #

import sqlite_manager_client_helper as helper
import socket
import time


if __name__ == "__main__":
    m = helper.SqliteManager(address=('127.0.0.1', 50001), authkey='123456')
    try:
        m.connect()
    except socket.error as _:
        raise Exception("服务连接超时")

    start = time.time()
    for i in xrange(10):
        helper.execute_batch(m, [{"method": helper.ExecuteSqlMethod.execute, "sql": "select * from book;", "param": []}],
                             helper.ExecuteSqlResultMethod.fetchall, timeout=2)
    print("多次请求,查询10次,耗时:"+str(time.time() - start)+"s")

    start = time.time()
    for i in xrange(10):
        helper.execute_batch(m, [
            {"method": helper.ExecuteSqlMethod.execute,
             "sql": "insert into book(title,author,published) VALUES(?,?,?);",
             "param": [str(i), "xm", "xm"]}],
                             helper.ExecuteSqlResultMethod.rowcount, timeout=2)
    print("多次请求,更新10条,耗时:" + str(time.time() - start) + "s")

    start = time.time()
    helper.execute_batch(m, [
        {"method": helper.ExecuteSqlMethod.executemany,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [
             [str(1), "xm", "xm"],
             [str(2), "xm", "xm"],
             [str(3), "xm", "xm"],
             [str(4), "xm", "xm"],
             [str(5), "xm", "xm"],
             [str(6), "xm", "xm"],
             [str(7), "xm", "xm"],
             [str(8), "xm", "xm"],
             [str(9), "xm", "xm"],
             [str(10), "xm", "xm"]
         ]}], helper.ExecuteSqlResultMethod.rowcount, timeout=2)
    print("单次请求,批量更新10条,耗时:" + str(time.time() - start) + "s")

    start = time.time()
    helper.execute_batch(m, [
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(1), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(2), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(3), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(4), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(5), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(6), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(7), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(8), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(9), "xm", "xm"]},
        {"method": helper.ExecuteSqlMethod.execute,
         "sql": "insert into book(title,author,published) VALUES(?,?,?);",
         "param": [str(10), "xm", "xm"]}
    ], helper.ExecuteSqlResultMethod.rowcount, timeout=2)
    print("单次请求,批量执行10条更新,耗时:" + str(time.time() - start) + "s")
    helper.stop_server(m)