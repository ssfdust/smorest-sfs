"""
    smorest_sfs.modules.codes.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    编码模块的Schemas
"""
from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal.bases import BaseMsgSchema


class TypeCodeSchema(Schema):
    type_code = fields.Str()


class CodeOptsSchema(Schema):
    """编码的选项"""

    class Meta:
        fields = ("id", "name")


class NestedCodeSchema(Schema):

    children = fields.List(fields.Nested("NestedCodeSchema"))

    class Meta:
        fields = ("id", "name", "children")


class CodeListSchema(BaseMsgSchema):
    """编码的选项列表"""

    data = fields.List(fields.Nested(NestedCodeSchema))
