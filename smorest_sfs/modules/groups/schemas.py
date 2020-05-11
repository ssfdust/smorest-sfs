"""
    smorest_sfs.modules.groups.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户组模块的Schemas
"""
from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal import (
    auto_field,
    BaseMsgSchema,
    BasePageSchema,
    SQLAlchemySchema,
    SQLAlchemyAutoSchema,
)

from . import models


class GroupSchema(SQLAlchemySchema):
    """
    用户组的序列化类
    """
    id = auto_field(dump_only=True)
    name = auto_field()
    default = auto_field()
    description = auto_field()
    roles = auto_field()
    users = auto_field(dump_only=True)

    class Meta:
        model = models.Group
        load_instance = True


class GroupUserSchema(SQLAlchemySchema):
    """
    用户组的序列化类
    """
    users = auto_field(load_only=True)

    class Meta:
        model = models.Group
        load_instance = True


class GroupPageSchema(BasePageSchema):
    """用户组的分页"""

    data = fields.List(fields.Nested(GroupSchema))


class GroupItemSchema(BaseMsgSchema):
    """用户组的单项"""

    data = fields.Nested(GroupSchema)


class GroupOptsSchema(Schema):
    """用户组的选项"""

    class Meta:
        fields = ("id", "name")


class GroupListSchema(Schema):
    """用户组的选项列表"""

    data = fields.List(fields.Nested(GroupOptsSchema))
