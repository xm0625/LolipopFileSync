# -*- coding: utf-8 -*-
__version__ = '0.1'

import sys
import os
from bottle import Bottle, TEMPLATE_PATH

app = Bottle(autojson=False)
app_root_path = sys.path[0]
TEMPLATE_PATH.append(os.path.join(app_root_path, "project", "views"))
TEMPLATE_PATH.remove("./views/")
from project.controller import *
