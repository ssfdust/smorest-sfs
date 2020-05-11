"""
    smorest_sfs.modules.codes.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    编码的ORM模块
"""
from sqlalchemy_mptt.mixins import BaseNestedSets

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db


class Code(Model, SurrogatePK, BaseNestedSets):
    """
    编码

    :attr name: str(128) 编码名称
    """

    __tablename__ = "codes"

    name = db.Column(db.String(length=128), nullable=False, doc="编码名称")
    type_code = db.Column(db.String(length=16), nullable=False, doc="类型码")

    def __repr__(self) -> str:
        return self.name
