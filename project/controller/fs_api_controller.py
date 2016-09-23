# -*- coding: utf-8 -*-
from project import app
from project.decorator.cors import allow_cross_domain
from project.decorator.response_format import response_wrapped_json
from project.decorator.response_format import response_json
from project.decorator.global_exception_handler import global_exception_handler
from project.decorator.local_ip_check import local_ip_check
from project.bottle import request
from project.exception.common_exception import CommonException
from project.service import fs_api_service
import os


@app.route('/api/fs/list_dir', method=['GET', 'POST'])
@allow_cross_domain
@response_json
@global_exception_handler
@local_ip_check
def list_dir():
    dir_id = request.params.get('id')
    return fs_api_service.list_dir(dir_id)


@app.route('/api/fs/reload', method=['GET', 'POST'])
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
@local_ip_check
def reload_dir():
    fs_api_service.reload_dir()
    return "ok"


@app.route('/api/fs/walkPath', method=['GET', 'POST'])
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
@local_ip_check
def walk_path():
    path_to_walk = request.params.get('path')
    return fs_api_service.walk_and_gen_path_info(path_to_walk)


@app.route('/api/fs/diffPathInfo', method=['GET', 'POST'])
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
@local_ip_check
def walk_path():
    local_path_info = request.params.get('localPathInfo')
    remote_path_info = request.params.get('remotePathInfo')
    return fs_api_service.diff_path_info(local_path_info, remote_path_info)



