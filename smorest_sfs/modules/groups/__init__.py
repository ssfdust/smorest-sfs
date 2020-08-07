#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.groups
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    用户组模块
"""
from typing import Dict

from flask_smorest import Blueprint

blp = Blueprint("Group", __name__, url_prefix="/groups", description="用户组模块")

ma_mapping: Dict[str, str] = dict(
    [
        (
            "smorest_sfs.modules.groups.models.Group",
            "smorest_sfs.modules.groups.schemas.GroupSchema",
        )
    ]
)
