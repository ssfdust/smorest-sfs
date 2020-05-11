#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    smorest_sfs.modules.users.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    用户的ORM模块
"""
from __future__ import annotations

from marshmallow.validate import OneOf, Range
from sqlalchemy_utils.types import PasswordType

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db
from smorest_sfs.modules.groups.models import Group, groups_users
from smorest_sfs.modules.roles.models import permission_roles
from smorest_sfs.utils.sqla import RelateTableArgs, create_relation_table

roles_users = create_relation_table(
    db, RelateTableArgs("roles_users", "role_id", "user_id")
)

user_permissions = db.join(
    roles_users, permission_roles, roles_users.c.role_id == permission_roles.c.role_id
)


class User(Model, SurrogatePK):
    """
    用户表

    :attr username required: str(255) 用户名
    :attr email: str(255) 用户邮箱
    :attr password required: str(255) 用户密码
    :attr phonenum: str(255) 电话号码
    :attr active opt: bool 是否启用
    :attr confirmed_at: DateTime 确认时间
    :attr roles: Role 角色
    :attr permissions: Permission 权限
    :attr userinfo required: UserInfo 用户详情
    :attr groups: Group 用户组信息
    """

    __tablename__ = "users"

    username = db.Column(db.String(255), nullable=False, unique=True, doc="用户名")
    phonenum = db.Column(db.String(255), nullable=True, unique=True, doc="电话号码")
    email = db.Column(db.String(255), nullable=True, unique=True, doc="用户邮箱")
    password = db.Column(
        PasswordType(schemes=["pbkdf2_sha512"]), nullable=False, doc="用户密码"
    )
    active = db.Column(db.Boolean(), doc="启用", default=False)
    confirmed_at = db.Column(db.DateTime(), doc="确认时间")
    roles = db.relationship(
        "Role",
        secondary=roles_users,
        uselist=True,
        doc="所有角色",
        primaryjoin="foreign(roles_users.c.user_id) == User.id",
        secondaryjoin="foreign(roles_users.c.role_id) == Role.id",
        backref=db.backref("users", lazy="dynamic", doc="所有用户"),
        info={"marshmallow": {"column": ["id", "name"]}},
    )
    permissions = db.relationship(
        "Permission",
        secondary=user_permissions,
        doc="权限",
        primaryjoin="User.id == roles_users.c.user_id",
        secondaryjoin="Permission.id == permission_roles.c.permission_id",
        viewonly=True,
        info={"marshmallow": {"dump_only": True, "column": ["id", "name"]}},
    )
    userinfo = db.relationship(
        "UserInfo",
        doc="用户",
        primaryjoin="User.id == UserInfo.uid",
        foreign_keys="UserInfo.uid",
        uselist=False,
        lazy="joined",
        info={
            "marshmallow": {
                "column": ["avator_id", "first_name", "last_name", "sex", "age"]
            }
        },
    )
    groups = db.relationship(
        Group,
        secondary=groups_users,
        primaryjoin="User.id == groups_users.c.user_id",
        secondaryjoin=Group.id == groups_users.c.group_id,
        doc="组下用户",
        foreign_keys=[groups_users.c.group_id, groups_users.c.user_id],
        info={"marshmallow": {"column": ["id", "name"]}},
    )

    @classmethod
    def get_by_keyword(cls, keyword: str) -> User:
        """
        根据邮箱获取用户
        """
        return cls.query.filter(
            db.or_(
                cls.email == keyword, cls.username == keyword, cls.phonenum == keyword,
            ),
        ).first_or_404()

    def __repr__(self) -> str:  # pragma: no cover
        return self.nickname

    @property
    def nickname(self) -> str:
        return self.userinfo.nickname


class UserInfo(SurrogatePK, Model):
    """
    用户信息表

    :attr avator_id: int 用户头像ID
    :attr uid: int 用户ID
    :attr avator: Storages 用户头像
    :attr user: User 关联用户
    :attr sex: int 性别
    :attr age: int 年龄
    :attr first_name: str(80) 姓
    :attr second_name: str(80) 名
    """

    __tablename__ = "userinfo"

    avator_id = db.Column(
        db.Integer, doc="头像ID", info={"marshmallow": {"dump_only": True}}
    )
    uid = db.Column(db.Integer, doc="用户ID", info={"marshmallow": {"dump_only": True}})
    sex = db.Column(
        db.Integer,
        doc="性别",
        default=1,
        info={
            "marshmallow": {
                "validate": [OneOf([1, 2])],
                "allow_none": False,
                "required": True,
            }
        },
    )
    age = db.Column(
        db.Integer,
        doc="年龄",
        info={
            "marshmallow": {
                "allow_none": False,
                "validate": [Range(1, None)],
                "required": True,
            }
        },
    )
    first_name = db.Column(
        db.String(80),
        doc="姓",
        info={"marshmallow": {"allow_none": False, "required": True}},
    )
    last_name = db.Column(
        db.String(80),
        doc="名",
        info={"marshmallow": {"allow_none": False, "required": True}},
    )
    user = db.relationship(
        "User",
        doc="用户",
        primaryjoin="User.id == UserInfo.uid",
        foreign_keys=uid,
        info={"marshmallow": {"dump_only": True}},
    )
    avator = db.relationship(
        "Storages",
        primaryjoin="Storages.id == UserInfo.avator_id",
        foreign_keys=avator_id,
        doc="头像",
        lazy="joined",
        info={"marshmallow": {"dump_only": True}},
    )

    def __repr__(self) -> str:
        return self.nickname

    @property
    def nickname(self) -> str:
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        return self.user.username

    @property
    def sex_label(self) -> str:
        """性别标签"""
        labels = {1: "男", 2: "女"}
        try:
            return labels[self.sex]
        except KeyError:
            return "未填写"
