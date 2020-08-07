#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    smorest_sfs.extensions.sqla.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    辅助函数模块
"""

from typing import Any

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):  # type: ignore
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(_: Any, __: Any, **kw: Any) -> str:
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
