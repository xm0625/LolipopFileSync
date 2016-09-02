#!/usr/bin/python
# -*- conding:utf-8 -*-
from project.bottle import *


def allow_cross_domain(fn):
    def __wrapper(*args, **kwargs):
        # set cross headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,OPTIONS'
        allow_headers = 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,' \
                        'Cache-Control,Content-Type'
        response.headers['Access-Control-Allow-Headers'] = allow_headers
        return fn(*args, **kwargs)

    return __wrapper
