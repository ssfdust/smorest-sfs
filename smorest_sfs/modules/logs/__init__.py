#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.logs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    日志模块
"""
from flask_smorest import Blueprint

blp = Blueprint("Log", __name__, url_prefix="/logs", description="日志模块")
