"""
    smorest_sfs.modules.menus.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    菜单模块的Schemas
"""
from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal import (
    BaseMsgSchema,
    IdFiledSchema,
    SQLAlchemySchema,
    auto_field,
)
from smorest_sfs.modules.users.schemas import PermissionInfoSchema

from . import models


class MenuSchema(SQLAlchemySchema, IdFiledSchema):
    """
    菜单的序列化类
    """

    name = auto_field()
    url = auto_field()
    img = auto_field()
    children = fields.List(fields.Nested("MenuSchema"), dump_only=True)
    parent_id = fields.Int()
    permission = fields.Nested(PermissionInfoSchema, load_only=True)

    class Meta:
        model = models.Menu


class MenuOptsSchema(Schema):
    """菜单的选项"""

    class Meta:
        fields = ("id_", "name", "url", "img")


class MenuListSchema(BaseMsgSchema):
    """菜单的选项列表"""

    data = fields.List(fields.Nested(MenuSchema))
