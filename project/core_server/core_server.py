# coding=utf-8

# 解决py2.7中文出现write错误的问题
import sys

from project.util.byteify import byteify

reload(sys)
sys.setdefaultencoding('utf-8')
# 解决py2.7中文出现write错误的问题 #

# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
import urlparse
import json

max_id = 0
id_path_map = {}
config = {}

class CommonException(Exception):
    code = "0"
    message = "system busy"
    """docstring for CommonException"""

    def __init__(self, code, message="system busy"):
        super(CommonException, self).__init__()
        if code:
            self.code = code
        if message:
            self.message = message


def execute(request):
    global max_id
    global id_path_map
    if "task_obj" not in request.keys():
        raise CommonException("-1", "缺少task_obj")
    task_obj_string = request["task_obj"]
    task_obj = byteify(json.loads(task_obj_string))

    method = task_obj["method"]
    param = task_obj["param"]
    if method == "getStartId":
        id_num = param["idNum"]
        old_max_id = max_id
        max_id += id_num
        return old_max_id
    if method == "putIdPathMap":
        print(param)
        for id_string in param:
            id_path_map[id_string] = param[id_string]
        return "ok"
    if method == "getPath":
        id_string = param["id"]
        return id_path_map[str(id_string)]
    if method == "reloadDir":
        id_path_map = {}
        max_id = 0
        return "ok"
    if method == "getConfig":
        key = param["key"]
        default_value = None
        if "default" in param:
            default_value = param["default"]
        if key not in config:
            return default_value
        return config[key]
    if method == "updateConfig":
        key = param["key"]
        value = param["value"]
        config[key] = value
        return "ok"
    if method == "saveConfig":
        with open("./config.json", 'w+') as f:
            config_content = json.dumps(config, ensure_ascii=False, indent=True)
            f.write(config_content)
        return "ok"


def app(environ, start_response):
    request_method = environ["REQUEST_METHOD"]  # GET
    path_info = environ["PATH_INFO"]  # /hi/name/index.action
    query_string = environ["QUERY_STRING"]  # ?后面的东西
    remote_address = environ["REMOTE_ADDR"]  # 访问者ip
    print "request_method:" + request_method
    print "path_info:" + path_info
    print "remote_address:" + remote_address

    if request_method == "GET":
        request = urlparse.parse_qs(query_string)
    else:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        request = urlparse.parse_qs(request_body)
    for (d, x) in request.items():
        if isinstance(x, list) and len(x) == 1:
            request[d] = x[0]
    for (d, x) in request.items():
        print "key:" + d + ",value:" + str(x)

    if path_info == "/":
        response_string = ""
        response_code = "200 OK"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
        try:
            fetch_result = "ok"
            response_data = {"code": "0", "message": "success", "result": fetch_result}
            response_string = json.dumps(response_data, ensure_ascii=False)
        except CommonException as ce:
            response_string = '{"code":"' + ce.code + '","message":"' + ce.message + '"}'
        except ValueError:
            import traceback
            traceback.print_exc()
            response_string = '{"code":"-1","message":"system busy"}'
    elif path_info == "/execute":
        response_string = ""
        response_code = "200 OK"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
        try:
            result = execute(request)
            response_data = {"code": "0", "message": "success", "result": result}
            response_string = json.dumps(response_data, ensure_ascii=False)
        except CommonException as ce:
            response_string = '{"code":"' + ce.code + '","message":"' + ce.message + '"}'
        except ValueError:
            import traceback
            traceback.print_exc()
            response_string = '{"code":"-1","message":"system busy"}'
    else:
        response_string = "404 NOT FOUND"
        response_code = "404 NOT FOUND"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
    start_response(response_code, response_header)
    return [byteify(response_string)]


def init():
    global config
    with open("./config.json") as f:
        config_content = f.read()
    config = json.loads(config_content)
    pass


def run():
    init()
    httpd = make_server('127.0.0.1', 50002, app)
    print "Serving HTTP on port 50001..."
    # 开始监听HTTP请求:
    httpd.serve_forever()


if __name__ == "__main__":
    run()
