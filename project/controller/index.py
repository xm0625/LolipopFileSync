# -*- coding: utf-8 -*-
from project import app
from project.bottle import template, redirect


@app.route('/', method='GET')
def index():
    redirect("/static/index.html")

