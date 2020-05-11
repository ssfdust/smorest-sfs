#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.roles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    角色权限模块
"""
from flask_smorest import Blueprint

blp = Blueprint("Role", __name__, url_prefix="/roles", description="角色管理模块")
