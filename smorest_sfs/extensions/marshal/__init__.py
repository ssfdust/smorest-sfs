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

from .bases import (
    BaseIntListSchema,
    BaseMsgSchema,
    BasePageSchema,
    BaseTimeParam,
    GeneralParam,
    UploadField,
)
from .ma import Marshmallow, SQLAlchemyAutoSchema, SQLAlchemySchema

ma = Marshmallow()

__all__ = [
    "ma",
    "auto_field",
    "SQLAlchemySchema",
    "Marshmallow",
    "SQLAlchemyAutoSchema",
    "BaseTimeParam",
    "BaseMsgSchema",
    "BasePageSchema",
    "BaseIntListSchema",
    "UploadField",
    "GeneralParam",
]
