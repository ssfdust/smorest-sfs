#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    smorest_sfs.extensions.sqla.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    辅助函数模块
"""

from datetime import datetime
from typing import Any

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime

from .model import Model


def set_default_for_instance(instance: Model) -> Model:
    """为修改时间，创建时间，删除设置默认值"""
    for key in ["modified", "created"]:
        setattr(instance, key, datetime.utcnow())
    setattr(instance, "deleted", False)
    return instance


class utcnow(expression.FunctionElement):  # type: ignore
    # pylint: disable=R0901,C0115
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(_: Any, __: Any, **kw: Any) -> str:
    # pylint: disable=W0613,C0116
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
