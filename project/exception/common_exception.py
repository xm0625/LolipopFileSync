#!/usr/bin/python
# -*- conding:utf-8 -*-


class CommonException(Exception):
    code = "0"
    message = "system busy"
    """docstring for CommonException"""
    def __init__(self, code=0, message="system busy"):
        Exception.__init__(self)
        if code:
            self.code = code
        if message:
            self.message = message
