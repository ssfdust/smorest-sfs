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
    smorest_sfs.modules.roles.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    角色权限的资源模块
"""
from typing import Any, Dict, List

from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_sqlalchemy import BaseQuery
from loguru import logger

from smorest_sfs.extensions import db
from smorest_sfs.extensions.api.decorators import paginate
from smorest_sfs.extensions.marshal.bases import (
    BaseIntListSchema,
    BaseMsgSchema,
    GeneralParam,
)
from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.auth.decorators import doc_login_required, permission_required
from smorest_sfs.plugins.samanager import SqlaManager

from . import blp, models, schemas

samanager: SqlaManager[models.Role] = SqlaManager(db.session)


@blp.route("/options")
class RoleListView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.RoleQuery)
    @blp.response(200, schemas.RoleListSchema)
    def get(self) -> Dict[str, List[models.Role]]:
        """
        获取所有角色权限选项信息
        """
        query = models.Role.query

        items = query.all()

        return {"data": items}


@blp.route("")
class RoleView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.RoleQuery)
    @blp.arguments(GeneralParam, location="query", as_kwargs=True)
    @blp.response(200, schemas.RolePageSchema)
    @paginate()
    def get(self, **kwargs: Dict[str, Any]) -> "BaseQuery[models.Role]":
        # pylint: disable=unused-argument
        """
        获取所有角色权限信息——分页
        """
        query = models.Role.where(**kwargs)

        return query

    @doc_login_required
    @permission_required(PERMISSIONS.RoleAdd)
    @blp.arguments(schemas.RoleSchema)
    @blp.response(200, schemas.RoleItemSchema)
    def post(self, role: models.Role) -> Dict[str, models.Role]:
        # pylint: disable=unused-argument
        """
        新增角色权限信息
        """
        role.save()
        logger.info(f"{current_user.username}新增了角色权限{role}")
        db.session.commit()

        return {"data": role}

    @doc_login_required
    @permission_required(PERMISSIONS.RoleDelete)
    @blp.arguments(BaseIntListSchema, as_kwargs=True)
    @blp.response(200, BaseMsgSchema)
    def delete(self, lst: List[int]) -> None:
        # pylint: disable=unused-argument
        """
        批量删除角色权限
        -------------------------------
        :param lst: list 包含id列表的字典
        """
        models.Role.destroy(*lst)
        logger.info(f"{current_user.username}删除了角色权限{lst}")
        db.session.commit()


@blp.route(
    "/<int:role_id>",
    parameters=[{"in": "path", "name": "role_id", "description": "角色权限id"}],
)
class RoleItemView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.RoleEdit)
    @blp.arguments(schemas.RoleSchema)
    @blp.response(200, schemas.RoleItemSchema)
    def put(self, role: models.Role, role_id: int) -> Dict[str, models.Role]:
        """
        更新角色权限
        """
        samanager.pk_with(models.Role, role_id)
        role = samanager.update_with(role)
        logger.info(f"{current_user.username}更新了角色权限{role.id_}")
        db.session.commit()

        return {"data": role}

    @doc_login_required
    @permission_required(PERMISSIONS.RoleDelete)
    @blp.response(200, BaseMsgSchema)
    def delete(self, role_id: int) -> None:
        """
        删除角色权限
        """
        models.Role.destroy(role_id)
        logger.info(f"{current_user.username}删除了角色权限{role_id}")
        db.session.commit()

    @doc_login_required
    @permission_required(PERMISSIONS.RoleQuery)
    @blp.response(200, schemas.RoleItemSchema)
    def get(self, role_id: int) -> Dict[str, models.Role]:
        # pylint: disable=unused-argument
        """
        获取单条角色权限
        """
        role = models.Role.find_or_fail(role_id)

        return {"data": role}
