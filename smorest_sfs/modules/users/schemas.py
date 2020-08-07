#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright
# Author:
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    app.modules.users.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户模块的Schemas
"""

from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Range

from smorest_sfs.extensions.marshal import (
    SQLAlchemyAutoSchema,
    SQLAlchemySchema,
    auto_field,
)
from smorest_sfs.extensions.marshal.bases import (
    BaseMsgSchema,
    BasePageSchema,
    WritableIdNameSchema,
)
from smorest_sfs.modules.groups.models import Group
from smorest_sfs.modules.roles.models import Permission, Role

from . import models


class UserInfoSchema(SQLAlchemyAutoSchema):

    avator_id = auto_field(dump_only=True)
    uid = auto_field(dump_only=True)
    sex = auto_field(validate=[OneOf([1, 2])], allow_none=False, required=True)
    age = auto_field(validate=[Range(1, None)], allow_none=False, required=True)
    first_name = auto_field(allow_none=False, required=True)
    last_name = auto_field(allow_none=False, required=True)

    class Meta:
        model = models.UserInfo


class RoleInfoSchema(SQLAlchemySchema, WritableIdNameSchema):
    class Meta:
        model = Role


class PermissionInfoSchema(SQLAlchemySchema, WritableIdNameSchema):
    class Meta:
        model = Permission


class GroupInfoSchema(SQLAlchemySchema, WritableIdNameSchema):
    class Meta:
        model = Group


class UserParam(Schema):
    """
    用户查询参数
    """

    username = fields.Str(description="用户名相关信息")


class UserLoadSchema(SQLAlchemySchema):

    id_ = fields.Int(data_key="id")

    class Meta:
        model = models.User


class UserSchema(SQLAlchemyAutoSchema):
    """
    用户的序列化类
    """

    id_ = auto_field(data_key="id", dump_only=True)
    nickname = fields.Str(dump_only=True)
    roles = fields.List(fields.Nested(RoleInfoSchema))
    permissions = fields.List(fields.Nested(PermissionInfoSchema))
    groups = fields.List(fields.Nested(GroupInfoSchema))
    userinfo = fields.Nested(UserInfoSchema)

    class Meta:
        include_relationships = True
        include_fk = True
        model = models.User
        exclude = ["password"]


class UserRegisterSchema(SQLAlchemyAutoSchema):
    """
    用户的序列化类
    """

    id_ = fields.Int(data_key="id", dump_only=True)
    nickname = fields.Str(dump_only=True)

    class Meta:
        include_relationships = True
        include_fk = True
        model = models.User
        exlcude = ["password"]


class UserSelfSchema(SQLAlchemyAutoSchema):
    """
    用户的序列化类
    """

    id_ = fields.Int(data_key="id", dump_only=True)
    nickname = fields.Str(dump_only=True)

    class Meta:
        model = models.User
        dump_only = ["roles", "active", "confirmed_at", "username"]


class UserPageSchema(BasePageSchema):
    """用户的分页"""

    data = fields.List(fields.Nested(UserSchema))


class UserItemSchema(BaseMsgSchema):
    """用户的单项"""

    data = fields.Nested(UserSchema)


class UserOptsSchema(Schema):
    """用户的选项"""

    id_ = fields.Int(data_key="id", dump_only=True)

    class Meta:
        fields = ("id_", "nickname")


class UserListSchema(BaseMsgSchema):
    """用户的选项列表"""

    data = fields.List(fields.Nested(UserOptsSchema))
