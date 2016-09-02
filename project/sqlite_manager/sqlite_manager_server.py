# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys
import threading

import time

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #

from multiprocessing.managers import BaseManager
from multiprocessing import Pipe
import Queue
import sqlite3

pipe_notify_map = {}


def get_callback_pipe(transaction_id):
    receive_conn, send_conn = Pipe(False)
    pipe_notify_map[transaction_id] = {
        "receive_conn": receive_conn,
        "send_conn": send_conn,
        "create_time": int(time.time() * 1000)
    }
    return receive_conn


def start_manage_server(address, port, authkey):
    m = SqliteManager(address=(address, port), authkey=authkey)
    s = m.get_server()
    s.serve_forever()


def worker(queue):
    connection = sqlite3.connect("db.sqlite")
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS person;
        DROP TABLE IF EXISTS book;

        CREATE TABLE person(
            firstname,
            lastname,
            age
        );

        CREATE TABLE book(
            title,
            author,
            published
        );

        INSERT INTO book(title, author, published)
        VALUES (
            'Dirk Gently''s Holistic Detective Agency',
            'Douglas Adams',
            1987
        );
    """)

    while True:
        task_obj = queue.get(block=True)
        if "stop_server" in task_obj:
            cursor.close()
            connection.close()
            return
        execute_list = task_obj["execute_list"]
        transaction_id = task_obj["transaction_id"]
        execute_result_method = task_obj["result_method"]
        result = ""
        if transaction_id in pipe_notify_map:
            try:
                for execute_item in execute_list:
                    execute_item_method = execute_item["method"]
                    execute_item_sql = execute_item["sql"]
                    execute_item_param = execute_item["param"]
                    if execute_item_method == "execute":
                        cursor.execute(execute_item_sql, tuple(execute_item_param))
                    if execute_item_method == "executemany":
                        cursor.executemany(execute_item_sql, execute_item_param)
                    if execute_item_method == "executescript":
                        cursor.executescript(execute_item_sql)
                connection.commit()
                if execute_result_method == "fetchall":
                    result = cursor.fetchall()
                if execute_result_method == "rowcount":
                    result = cursor.rowcount
            except Exception as e:
                connection.rollback()
                result = "error," + str(e.message)
            send_conn = pipe_notify_map[transaction_id]["send_conn"]
            send_conn.send({"code": "-1" if (isinstance(result, basestring) and result.startswith("error")) else "0",
                            "result": result})


def close_callback_pipe(transaction_id):
    if transaction_id in pipe_notify_map:
        pipe_info = pipe_notify_map.pop(transaction_id)
        send_conn = pipe_info["send_conn"]
        send_conn.close()
        receive_conn = pipe_info["receive_conn"]
        receive_conn.close()


class SqliteManager(BaseManager):
    pass


def run(ip, port, auth_key):
    q = Queue.Queue(maxsize=-1)
    SqliteManager.register('get_queue', callable=lambda: q)
    SqliteManager.register('get_callback_pipe', callable=get_callback_pipe)
    SqliteManager.register('close_callback_pipe', callable=close_callback_pipe)
    manage_server_thread = threading.Thread(target=start_manage_server, args=(ip, port, auth_key,))
    manage_server_thread.setDaemon(True)
    manage_server_thread.start()
    print("manage_server_thread started.")

    # TODO 新增一个进程,定时扫描pipe_notify_map,将其中超过预定超时时间的pipe强制close掉,避免持有过多的pipe

    print("worker_thread started.")
    worker(q)


if __name__ == "__main__":
    run("127.0.0.1", 50001, "123456")
