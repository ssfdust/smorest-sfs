#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 ssfdust RedLotus
# Author: ssfdust RedLotus
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
    app.modules.email_templates.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    电子邮件模板的资源模块
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
from smorest_sfs.modules.email_templates.models import EmailTemplate
from smorest_sfs.plugins.samanager import SqlaManager

from . import blp, models, schemas

samanager: SqlaManager[EmailTemplate] = SqlaManager(db.session)


@blp.route("/options")
class EmailTemplateListView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.EmailTemplateQuery)
    @blp.response(200, schemas.EmailTemplateListSchema)
    def get(self) -> Dict[str, List[EmailTemplate]]:
        # pylint: disable=unused-argument
        """
        获取所有电子邮件模板选项信息
        """
        query = EmailTemplate.query

        items = query.all()

        return {"data": items}


@blp.route("")
class EmailTemplateView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.EmailTemplateQuery)
    @blp.arguments(GeneralParam, location="query", as_kwargs=True)
    @blp.response(200, schemas.EmailTemplatePageSchema)
    @paginate()
    def get(self, **kwargs: Dict[str, Any]) -> "BaseQuery[EmailTemplate]":
        # pylint: disable=unused-argument
        """
        获取所有电子邮件模板信息——分页
        """
        query = EmailTemplate.where(**kwargs)

        return query

    @doc_login_required
    @permission_required(PERMISSIONS.EmailTemplateAdd)
    @blp.arguments(schemas.EmailTemplateSchema)
    @blp.response(200, schemas.EmailTemplateItemSchema)
    def post(
        self, email_template: EmailTemplate, **kwargs: Any
    ) -> Dict[str, EmailTemplate]:
        # pylint: disable=unused-argument
        """
        新增电子邮件模板信息
        """
        email_template.save()
        logger.info(f"{current_user.username}新增了电子邮件模板{email_template}")
        db.session.commit()

        return {"data": email_template}

    @doc_login_required
    @permission_required(PERMISSIONS.EmailTemplateDelete)
    @blp.arguments(BaseIntListSchema, as_kwargs=False)
    @blp.response(200, BaseMsgSchema)
    def delete(self, lst: Dict[str, List[int]], **kwargs: Any) -> None:
        # pylint: disable=unused-argument
        """
        批量删除电子邮件模板
        -------------------------------
        :param lst: list 包含id列表的字典
        """
        models.EmailTemplate.destroy(*lst["lst"])
        logger.info(f"{current_user.username}删除了电子邮件模板{lst}")
        db.session.commit()


@blp.route(
    "/<int:email_template_id>",
    parameters=[{"in": "path", "name": "email_template_id", "description": "电子邮件模板id"}],
)
class EmailTemplateItemView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.EmailTemplateEdit)
    @blp.arguments(schemas.EmailTemplateSchema)
    @blp.response(200, schemas.EmailTemplateItemSchema)
    def put(
        self, email_template: EmailTemplate, email_template_id: int
    ) -> Dict[str, EmailTemplate]:
        # pylint: disable=unused-argument
        """
        更新电子邮件模板
        """
        samanager.pk_with(EmailTemplate, email_template_id)
        email_template = samanager.update_with(email_template)
        db.session.commit()

        return {"data": email_template}

    @doc_login_required
    @permission_required(PERMISSIONS.EmailTemplateDelete)
    @blp.response(200, BaseMsgSchema)
    def delete(self, email_template_id: int, **kwargs: Any) -> None:
        # pylint: disable=unused-argument
        """
        删除电子邮件模板
        """
        models.EmailTemplate.destroy(email_template_id)
        logger.info(f"{current_user.username}删除了电子邮件模板{email_template_id}")
        db.session.commit()

    @doc_login_required
    @permission_required(PERMISSIONS.EmailTemplateQuery)
    @blp.response(200, schemas.EmailTemplateItemSchema)
    def get(self, email_template_id: int, **kwargs: Any) -> Dict[str, EmailTemplate]:
        # pylint: disable=unused-argument
        """
        获取单条电子邮件模板
        """
        email_template = models.EmailTemplate.find_or_fail(email_template_id)

        return {"data": email_template}
