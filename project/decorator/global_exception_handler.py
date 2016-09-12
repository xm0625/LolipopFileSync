#!/usr/bin/python
# -*- conding:utf-8 -*-
from project.exception.common_exception import CommonException
import traceback


def global_exception_handler(fn):
    def __wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except CommonException as ce:
            return {"code": ce.code, "message": ce.message}
        except Exception as e:
            traceback.print_exc()
            commonException = CommonException()
            return {"code": commonException.code, "message": commonException.message}

    return __wrapper
