#!/usr/bin/python
# -*- conding:utf-8 -*-

from project.bottle import *
from project.exception.common_exception import CommonException
from project.core_server import core_server_helper


def local_ip_check(fn):
    def __wrapper(*args, **kwargs):
        # set cross headers
        if request.remote_addr != "127.0.0.1": ## not local access, need check password
            auth_key = request.params.get('auth_key')
            if auth_key is None:
                raise CommonException(-2, "auth_key is empty.")
            default_auth_key = core_server_helper.execute("getConfig", {"key": "auth_key"})
            if auth_key != default_auth_key:
                raise CommonException(-2, "auth_key is error.")
        return fn(*args, **kwargs)

    return __wrapper
