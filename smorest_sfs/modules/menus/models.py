"""
    smorest_sfs.modules.menus.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    菜单的ORM模块
"""
from flask_jwt_extended import current_user
from sqlalchemy_mptt import BaseNestedSets

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db
from smorest_sfs.extensions.sqla.softdelete import QueryWithSoftDelete


class Menu(Model, SurrogatePK, BaseNestedSets):
    """
    菜单

    :attr name: str(128) 菜单名称
    """

    __tablename__ = "menus"

    name = db.Column(db.String(length=128), nullable=False, doc="菜单名称")
    img = db.Column(db.String(512), doc="菜单图片")
    url = db.Column(db.String(512), doc="菜单URL")
    permission_id = db.Column(db.Integer)
    permission = db.relationship(
        "Permission",
        primaryjoin="Permission.id == Menu.permission_id",
        foreign_keys=permission_id,
        uselist=False,
        info={"marshmallow": {"column": ["name"]}},
    )

    def __repr__(self) -> str:
        return self.name


def menu_filter(menus: QueryWithSoftDelete) -> QueryWithSoftDelete:
    permission_idlst = [p.id for p in current_user.permissions]
    return menus.filter(Menu.permission_id.in_(permission_idlst))
