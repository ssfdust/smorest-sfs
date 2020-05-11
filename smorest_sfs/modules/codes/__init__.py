#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.codes
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    编码模块
"""
from flask_smorest import Blueprint

blp = Blueprint("Code", __name__, url_prefix="/codes", description="编码模块")
