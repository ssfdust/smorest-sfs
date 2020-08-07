"""
    app.extensions.marshal
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    提供拓展的flask-marshmallow模块以更好地适应项目

    使用：
    >>> from app.extensions.marshal import ma
    >>> from flask import Flask
    >>> app = Flask('')
    >>> ma.init_app(app)
    >>> class SampleSchema(ma.Schema):
            id = fields.Int()
"""
from flask_marshmallow.sqla import auto_field
from marshmallow.validate import Length

from .bases import (
    BaseIntListSchema,
    BaseMsgSchema,
    BasePageSchema,
    BaseTimeParam,
    GeneralParam,
    IdFiledSchema,
    IdNameSchema,
    UploadField,
)
from .ma import Marshmallow, SQLAlchemyAutoSchema, SQLAlchemySchema

ma = Marshmallow()
not_empty = Length(min=1)

__all__ = [
    "ma",
    "not_empty",
    "auto_field",
    "SQLAlchemySchema",
    "Marshmallow",
    "SQLAlchemyAutoSchema",
    "BaseTimeParam",
    "BaseMsgSchema",
    "BasePageSchema",
    "BaseIntListSchema",
    "IdNameSchema",
    "UploadField",
    "GeneralParam",
    "IdFiledSchema",
]
