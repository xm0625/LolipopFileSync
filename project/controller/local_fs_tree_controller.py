# -*- coding: utf-8 -*-
from project import app
from project.decorator.cors import allow_cross_domain
from project.decorator.response_format import response_json
from project.decorator.response_format import response_normal_json
from project.decorator.global_exception_handler import global_exception_handler
from project.bottle import request
from project.exception.common_exception import CommonException
from project.service import local_fs_tree_service
import os


@app.route('/api/local/list_dir', method=['GET', 'POST'])
@allow_cross_domain
@response_normal_json
@global_exception_handler
def list_dir():
    dir_id = request.params.get('id')
    return local_fs_tree_service.list_dir(dir_id)


@app.route('/api/local/reload', method=['GET', 'POST'])
@allow_cross_domain
@response_json
@global_exception_handler
def reload_dir():
    local_fs_tree_service.reload_dir()
    return "ok"
