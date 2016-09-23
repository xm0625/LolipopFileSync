# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #
import urllib2
import urllib
import json

_url = "http://127.0.0.1:50002/execute"


def execute(method, param):
    task_obj = {
        "method": method,
        "param": param
    }
    req = urllib2.Request(_url, urllib.urlencode({"task_obj": json.dumps(task_obj, ensure_ascii=False)}))
    response = urllib2.urlopen(req)
    content = response.read()
    content_obj = json.loads(content)
    return content_obj["result"]
