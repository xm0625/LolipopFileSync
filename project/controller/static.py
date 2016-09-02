# -*- coding: utf-8 -*-
from project import app, app_root_path
from project.bottle import static_file
import os


@app.route('/static/<path:path>', method=['GET', 'POST'])
def server_all_static(path):
    return static_file(path, root=os.path.join(app_root_path, 'project', 'static'))

