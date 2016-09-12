# -*- coding: utf-8 -*-
from project import app
from project.decorator.cors import allow_cross_domain
from project.decorator.response_format import response_wrapped_json
from project.decorator.global_exception_handler import global_exception_handler
from project.decorator.local_ip_check import local_ip_check


@app.route('/api/version', method=['GET', 'POST'])
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
@local_ip_check
def get_version():
    return "v1.0"
