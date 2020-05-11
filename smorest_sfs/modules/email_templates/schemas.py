"""
    smorest_sfs.modules.email_templates.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    电子邮件模板模块的Schemas
"""
from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal import (
    SQLAlchemyAutoSchema,
    SQLAlchemySchema,
    auto_field,
)
from smorest_sfs.extensions.marshal.bases import BaseMsgSchema, BasePageSchema

from . import models


class EmailTemplateSchema(SQLAlchemyAutoSchema):
    """
    电子邮件模板的序列化类
    """

    class Meta:
        model = models.EmailTemplate


class EmailTemplatePageSchema(BasePageSchema):
    """电子邮件模板的分页"""

    data = fields.List(fields.Nested(EmailTemplateSchema))


class EmailTemplateItemSchema(BaseMsgSchema):
    """电子邮件模板的单项"""

    data = fields.Nested(EmailTemplateSchema)


class EmailTemplateOptsSchema(Schema):
    """电子邮件模板的选项"""

    class Meta:
        fields = ("id", "name")


class EmailTemplateListSchema(Schema):
    """电子邮件模板的选项列表"""

    data = fields.List(fields.Nested(EmailTemplateOptsSchema))
