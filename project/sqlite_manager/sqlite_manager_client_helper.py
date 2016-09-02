# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #

# 设置连接超时
import time
from multiprocessing import managers, connection
sys.modules['multiprocessing'].__dict__['managers'].__dict__['connection']._init_timeout = lambda: time.time() + 2
# 设置连接超时 #

from multiprocessing.managers import BaseManager
import socket
import uuid # str(uuid.uuid1()).replace("-","")
from project.exception.common_exception import CommonException

class SqliteManager(BaseManager):
    pass

SqliteManager.register('get_queue')
SqliteManager.register('get_callback_pipe')
SqliteManager.register('close_callback_pipe')


class ExecuteSqlMethod(object):
    execute = "execute"
    executemany = "executemany"
    executescript = "executescript"


class ExecuteSqlResultMethod(object):
    fetchall = "fetchall"
    rowcount = "rowcount"


def execute_batch(sqlite_manager, execute_list, result_method, timeout=30):
    transaction_id = str(uuid.uuid1()).replace("-", "")
    try:
        queue = sqlite_manager.get_queue()
        receive_conn = sqlite_manager.get_callback_pipe(transaction_id)
        task_data = {
            "transaction_id": transaction_id,
            "execute_list": execute_list,
            "result_method": result_method
        }
        queue.put(task_data)
        if not receive_conn.poll(timeout):
            raise CommonException("0", "等待超时")
        result = receive_conn.recv()
        # print("result received. result=" + str(result["result"]))
        if "code" not in result:
            raise CommonException("0", "服务异常")
        if result["code"] != "0":
            raise CommonException("0", "数据库执行失败 error="+str(result["result"]))
        return result["result"]
    except socket.error as _:
        raise CommonException("0", "与服务失去连接")
    except EOFError as _:
        raise CommonException("0", "与服务失去连接")
    finally:
        try:
            sqlite_manager.close_callback_pipe(transaction_id)
        except socket.error as _:
            pass
        except EOFError as _:
            pass


def execute_sql(sqlite_manager, method, sql, param, result_method, timeout=30):
    return execute_batch(sqlite_manager, [{"method": method, "sql": sql, "param": param}], result_method,
                         timeout=timeout)


def stop_server(sqlite_manager):
    try:
        queue = sqlite_manager.get_queue()
        task_data = {
            "stop_server": 1
        }
        queue.put(task_data)
    except socket.error as _:
        pass
    except EOFError as _:
        pass
    return "ok"

