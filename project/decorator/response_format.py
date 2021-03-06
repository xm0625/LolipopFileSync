#!/usr/bin/python
# -*- conding:utf-8 -*-
from project.bottle import response
import json

__author__ = 'xm'


def response_wrapped_json(fn):
    def __wrapper(*args, **kwargs):
        response_data = fn(*args, **kwargs)
        response.content_type = 'application/json; charset=' + response.charset
        if (response_data is not None) and ("code" in response_data) and ("message" in response_data):
            return json.dumps(response_data, encoding=response.charset)
        else:
            result_data = json.dumps({"code": "1", "message": "ok", "data": response_data}, encoding=response.charset)
            return result_data

    return __wrapper


def response_json(fn):
    def __wrapper(*args, **kwargs):
        response_data = fn(*args, **kwargs)
        response.content_type = 'application/json; charset=' + response.charset
        return json.dumps(response_data, encoding=response.charset)

    return __wrapper
