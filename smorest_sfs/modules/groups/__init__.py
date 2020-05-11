#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.groups
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    用户组模块
"""
from flask_smorest import Blueprint

blp = Blueprint("Group", __name__, url_prefix="/groups", description="用户组模块")
