#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.projects
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    项目模块
"""

from typing import Dict
from flask_smorest import Blueprint

blp = Blueprint("Project", __name__, url_prefix="/projects", description="项目模块",)

ma_mapping: Dict[str, str] = dict(
    [
        (
            "smorest_sfs.modules.projects.models.Project",
            "smorest_sfs.modules.projects.schemas.ProjectSchema",
        )
    ]
)
