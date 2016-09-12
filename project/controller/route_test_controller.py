# -*- coding: utf-8 -*-
from project import app, app_root_path
from project.bottle import template, request
from project.decorator.cors import allow_cross_domain
from project.decorator.global_exception_handler import global_exception_handler
from project.decorator.response_format import response_wrapped_json
from project.exception.common_exception import CommonException
from project.service import route_test_service
import os
import uuid


@app.route('/api/hello', method='GET')
@response_wrapped_json
def hello():
    return {"hello": "world"}


@app.route('/api/corTest', method=['GET', 'POST'])
@allow_cross_domain
@response_wrapped_json
def cor_test():
    return {"hello": "world"}


@app.route('/api/exceptionTest', method=['GET', 'POST'])
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
def exception_test():
    raise CommonException()
    return {"hello": "world"}


@app.route('/uploadTest', method='GET')
@response_wrapped_json
def do_upload():
    return template('upload/form', message='')


@app.route('/upload', method='POST')
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
def do_upload():
    category = request.params.get('category')
    upload_file = request.files.get('upload')
    print("upload_file.raw_filename:"+upload_file.raw_filename)
    name, ext = os.path.splitext(upload_file.raw_filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        raise CommonException('0', 'File extension not allowed. ext='+ext)
    new_file_name = str(uuid.uuid1()).replace("-", "") + ext
    upload_save_path = os.path.join(app_root_path, "project", "fileUpload", new_file_name)
    upload_file.save(upload_save_path)  # appends upload.filename automatically
    return {"category": category, "saveFileName": new_file_name}


@app.route('/api/helloTo', method=['GET', 'POST'])
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
def hello_to_somebody():
    username = request.params.get('username')
    return {"greeting": route_test_service.get_greeting_words(username)}


@app.route('/api/books', method=['GET', 'POST'])
@global_exception_handler
@allow_cross_domain
@response_wrapped_json
def get_all_books():
    return {"books": route_test_service.get_all_books()}


@app.route('/api/addBook', method=['GET', 'POST'])
@allow_cross_domain
@response_wrapped_json
@global_exception_handler
def add_books():
    title = request.params.get('book.title')
    author = request.params.get('book.author')
    published = request.params.get('book.published')
    route_test_service.add_books(title, author, published)
    return ""
