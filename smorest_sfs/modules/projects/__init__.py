#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.projects
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    项目模块
"""
from flask_smorest import Blueprint

blp = Blueprint("Project", __name__, url_prefix="/projects", description="项目模块")
