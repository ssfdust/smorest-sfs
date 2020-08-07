"""
    smorest_sfs.modules.groups.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    用户组的ORM模块
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy_mptt import BaseNestedSets

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db
from smorest_sfs.utils.sqla import RelateTableArgs, create_relation_table

if TYPE_CHECKING:
    from smorest_sfs.modules.users.models import User
    from smorest_sfs.modules.roles.models import Role

groups_users = create_relation_table(
    db, RelateTableArgs("groups_users", "group_id", "user_id")
)
groups_roles = create_relation_table(
    db, RelateTableArgs("groups_roles", "group_id", "role_id")
)


class Group(Model, SurrogatePK, BaseNestedSets):
    """
    用户组

    :attr name: str(128) 用户组名称
    :attr description str(255) 组描述
    :attr default bool 是否为初始化默认组
    :attr roles 所有角色
    :attr users 所有用户
    """

    sqlalchemy_mptt_pk_name = "id_"
    __tablename__ = "groups"

    name = db.Column(db.String(length=128), nullable=False, doc="用户组名称")
    description = db.Column(db.String(255), doc="组描述")
    default = db.Column(db.Boolean, default=False, doc="初始化默认组")
    users = db.relationship(
        "User",
        secondary="groups_users",
        primaryjoin="Group.id_ == groups_users.c.group_id",
        secondaryjoin="User.id_ == groups_users.c.user_id",
        doc="组下用户",
        foreign_keys="[groups_users.c.group_id, groups_users.c.user_id]",
        active_history=True,
        lazy="joined",
        info={"marshmallow": {"column": ["id", "username"]}},
    )
    roles = db.relationship(
        "Role",
        uselist=True,
        secondary="groups_roles",
        primaryjoin="Group.id_ == groups_roles.c.group_id",
        secondaryjoin="Role.id_ == groups_roles.c.role_id",
        doc="组下默认角色",
        foreign_keys="[groups_roles.c.group_id, groups_roles.c.role_id]",
        active_history=True,
        lazy="joined",
        info={"marshmallow": {"column": ["id", "name"]}},
    )

    @classmethod
    def get_by_name(cls, name: str) -> Group:
        return cls.where(name=name).first_or_404()

    def __repr__(self) -> str:
        return self.name
