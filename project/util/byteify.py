# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    elif isinstance(input, str):
        try:
            return input.decode('utf-8').encode('utf-8')
        except Exception:
            try:
                return input.decode('gbk').encode('utf-8')
            except Exception:
                return input
    else:
        return input