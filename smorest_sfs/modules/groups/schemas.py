"""
    smorest_sfs.modules.groups.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户组模块的Schemas
"""
from marshmallow import fields

from smorest_sfs.extensions.marshal import (
    BaseMsgSchema,
    BasePageSchema,
    IdFiledSchema,
    IdNameSchema,
    SQLAlchemySchema,
    auto_field,
)
from smorest_sfs.modules.users.schemas import RoleInfoSchema, UserLoadSchema

from . import models


class GroupSchema(SQLAlchemySchema, IdFiledSchema):
    """
    用户组的序列化类
    """

    name = auto_field()
    default = auto_field()
    description = auto_field()
    roles = fields.List(fields.Nested(RoleInfoSchema))
    users = fields.List(fields.Nested(IdNameSchema), dump_only=True)

    class Meta:
        model = models.Group
        load_instance = True


class GroupUserSchema(SQLAlchemySchema):
    """
    用户组的序列化类
    """

    users = fields.List(fields.Nested(UserLoadSchema), load_only=True)

    class Meta:
        model = models.Group
        load_instance = True


class GroupPageSchema(BasePageSchema):
    """用户组的分页"""

    data = fields.List(fields.Nested(GroupSchema))


class GroupItemSchema(BaseMsgSchema):
    """用户组的单项"""

    data = fields.Nested(GroupSchema)


class GroupListSchema(BaseMsgSchema):
    """用户组的选项列表"""

    data = fields.List(fields.Nested(IdNameSchema))
