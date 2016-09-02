#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #

# 从wsgiref模块导入:
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler, ServerHandler
from processPool.PooledProcessMixIn import PooledProcessMixIn
import threading
import os
from project import app
from project.bottle import debug, run
from project.sqlite_manager import sqlite_manager_server

debug(True)


# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
def start_httpd(host, port):
    global httpd_server

    class ProcessPoolWSGIServer(PooledProcessMixIn, WSGIServer):
        pass

        def finish_request(self, request, client_address):
            try:
                WSGIServer.finish_request(self, request, client_address)
            except IOError as ex:
                if ex.errno == 32:
                    print('client disconnected.')
                else:
                    raise ex

    class FixedServerHandler(ServerHandler):
        def finish_response(self):
            try:
                ServerHandler.finish_response(self)
            except IOError as ex:
                if ex.errno == 32:
                    print('client disconnected.')
                else:
                    raise ex

    class FixedWSGIRequestHandler(WSGIRequestHandler):
        def handle(self):
            """Handle a single HTTP request"""
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return

            if not self.parse_request():  # An error code has been sent, just exit
                return

            handler = FixedServerHandler(
                self.rfile, self.wfile, self.get_stderr(), self.get_environ()
            )
            handler.request_handler = self  # backpointer for logging
            handler.run(self.server.get_app())

    httpd_server = make_server(host, port, app, server_class=ProcessPoolWSGIServer,
                               handler_class=FixedWSGIRequestHandler)
    print('Started httpd %s' % port)
    httpd_server.serve_forever()



if __name__ == '__main__':
    httpd_thread = threading.Thread(target=start_httpd, args=("0.0.0.0", 8000,))
    httpd_thread.setDaemon(True)
    httpd_thread.start()
    print("httpd_thread started.")

    sqlite_manager_thread = threading.Thread(target=sqlite_manager_server.run, args=("127.0.0.1", 50001, "123456",))
    sqlite_manager_thread.setDaemon(True)
    sqlite_manager_thread.start()
    print("sqlite_manager_thread started.")
    sqlite_manager_thread.join()

    httpd_thread.join()
    # port = int(os.environ.get("PORT", 8080))
    # run(app, reloader=True, interval=1, host='0.0.0.0', port=port)
