"""
    smorest_sfs.modules.projects.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    项目模块的Schemas
"""
from smorest_sfs.extensions.marshal import (
    BasePageSchema,
    BaseMsgSchema,
    SQLAlchemyAutoSchema,
)
from marshmallow import fields, Schema

from . import models


class ProjectSchema(SQLAlchemyAutoSchema):
    """
    项目的序列化类
    """

    id_ = fields.Int(data_key="id", dump_only=True)

    class Meta:
        model = models.Project


class ProjectPageSchema(BasePageSchema):
    """项目的分页"""

    data = fields.List(fields.Nested(ProjectSchema))


class ProjectItemSchema(BaseMsgSchema):
    """项目的单项"""

    data = fields.Nested(ProjectSchema)


class ProjectOptsSchema(Schema):
    """项目的选项"""

    id_ = fields.Int(data_key="id")

    class Meta:
        fields = ("id_", "name")


class ProjectListSchema(BaseMsgSchema):
    """项目的选项列表"""

    data = fields.List(fields.Nested(ProjectOptsSchema))
