#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.menus
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    菜单模块
"""
from flask_smorest import Blueprint

blp = Blueprint("Menu", __name__, url_prefix="/menus", description="菜单模块")
