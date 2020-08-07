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
    app.modules.roles.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    角色权限模块的Schemas
"""

from marshmallow import fields

from smorest_sfs.extensions.marshal import (
    IdNameSchema,
    SQLAlchemyAutoSchema,
    SQLAlchemySchema,
)
from smorest_sfs.extensions.marshal.bases import (
    BaseMsgSchema,
    BasePageSchema,
    WritableIdNameSchema,
)

from . import models


class PermissionOptSchema(SQLAlchemySchema, WritableIdNameSchema):
    class Meta:
        model = models.Permission


class RoleSchema(SQLAlchemyAutoSchema, IdNameSchema):
    """
    角色权限的序列化类
    """

    permissions = fields.List(fields.Nested(PermissionOptSchema))

    class Meta:
        model = models.Role


class RolePageSchema(BasePageSchema):
    """角色权限的分页"""

    data = fields.List(fields.Nested(RoleSchema))


class RoleItemSchema(BaseMsgSchema):
    """角色权限的单项"""

    data = fields.Nested(RoleSchema)


class RoleListSchema(BaseMsgSchema):
    """角色权限的选项列表"""

    data = fields.List(fields.Nested(IdNameSchema))
