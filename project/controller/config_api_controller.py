# -*- coding: utf-8 -*-
import json

from project import app
from project.bottle import request
from project.decorator.cors import allow_cross_domain
from project.decorator.response_format import response_wrapped_json
from project.decorator.global_exception_handler import global_exception_handler
from project.decorator.local_ip_check import local_ip_check
from project.service import config_api_service


@app.route('/api/config/update', method='POST')
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
@local_ip_check
def update_config():
    key = request.params.get('key')
    value = request.params.get('value')
    is_json = request.params.get('isJson')
    config_api_service.update_config(key, json.loads(value) if is_json == "1" else value)
    return "ok"


@app.route('/api/config/save', method='GET')
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
@local_ip_check
def save_config():
    config_api_service.save_config()
    return "ok"


@app.route('/api/config/detail/<config_key>', method='GET')
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
@local_ip_check
def get_server_config(config_key):
    return config_api_service.get_config(config_key)

