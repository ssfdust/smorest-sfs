"""
    smorest_sfs.modules.menus.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    菜单模块的Schemas
"""
from marshmallow import Schema, fields

from smorest_sfs.extensions import ma
from smorest_sfs.extensions.marshal import BaseMsgSchema, SQLAlchemyAutoSchema

from . import models


class MenuSchema(SQLAlchemyAutoSchema):
    """
    菜单的序列化类
    """

    children = fields.List(fields.Nested("MenuSchema"))
    parent_id = fields.Int()

    class Meta:
        model = models.Menu
        exclude = ["permission_id", "level", "left", "tree_id", "parent", "right"]
        dump_only = ["id", "children"]
        load_only = ["permission"]
        session = models.db.session


class MenuOptsSchema(Schema):
    """菜单的选项"""

    class Meta:
        fields = ("id", "name", "url", "img")


class MenuListSchema(BaseMsgSchema):
    """菜单的选项列表"""

    data = fields.List(fields.Nested(MenuSchema))
