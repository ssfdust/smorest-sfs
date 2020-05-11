#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.users
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户模块
"""
from flask_smorest import Blueprint

blp = Blueprint("User", __name__, url_prefix="/users", description="用户管理模块")
