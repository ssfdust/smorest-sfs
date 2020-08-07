"""
    smorest_sfs.extensions.sqla.db
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    db实例模块
"""
from typing import TYPE_CHECKING

from flask_sqlalchemy import SQLAlchemy

from .model import Model

db = SQLAlchemy(model_class=Model)

if TYPE_CHECKING:
    BaseModel = db.make_declarative_base(Model)
else:
    BaseModel = db.Model

BaseModel.set_session(db.session)
