"""
    smorest_sfs.modules.logs.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    日志模块的Schemas
"""

from marshmallow import fields

from smorest_sfs.extensions.marshal import (
    BasePageSchema,
    BaseTimeParam,
    SQLAlchemyAutoSchema,
    SQLAlchemySchema,
    auto_field,
)

from . import models


class LogParam(SQLAlchemySchema, BaseTimeParam):
    """
    日志参数反序列化
    """

    module__contains = fields.Str(description="模块名称", data_key="module")
    level = auto_field(required=False)

    class Meta:
        model = models.Log
        load_instance = False


class RespLogParam(SQLAlchemySchema, BaseTimeParam):
    """
    响应日志参数反序列化
    """

    url__contains = fields.Str(description="url地址", data_key="url")
    method__ilike = fields.Str(description="方法", data_key="method")
    ip = auto_field(required=False)
    status_code = auto_field(required=False)

    class Meta:
        model = models.ResponseLog
        load_instance = False


class LogSchema(SQLAlchemyAutoSchema):
    """
    日志的序列化类
    """

    class Meta:
        model = models.Log


class RespLogSchema(SQLAlchemyAutoSchema):
    """
    响应日志的序列化类
    """

    class Meta:
        model = models.ResponseLog


class LogPageSchema(BasePageSchema):
    """日志的分页"""

    data = fields.List(fields.Nested(LogSchema))


class RespLogPageSchema(BasePageSchema):
    """日志的分页"""

    data = fields.List(fields.Nested(RespLogSchema))
