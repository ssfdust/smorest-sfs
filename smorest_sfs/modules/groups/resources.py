"""
    smorest_sfs.modules.groups.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户组的资源模块
"""
from typing import Any, Dict, List

from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_sqlalchemy import BaseQuery
from loguru import logger

from smorest_sfs.extensions import db
from smorest_sfs.extensions.api.decorators import paginate
from smorest_sfs.extensions.marshal.bases import BaseMsgSchema, GeneralParam
from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.auth.decorators import doc_login_required, permission_required
from smorest_sfs.plugins.samanager import SqlaManager
from smorest_sfs.services.groups import parse_group_change, parse_group_users_change

from . import blp, models, schemas

samanager: SqlaManager[models.Group] = SqlaManager(db.session)


@blp.route("/options")
class GroupListView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.GroupQuery)
    @blp.response(200, schemas.GroupListSchema)
    def get(self) -> Dict[str, List[models.Group]]:
        # pylint: disable=unused-argument
        """
        获取所有用户组选项信息
        """
        query = models.Group.query

        items = query.all()

        return {"data": items}


@blp.route("")
class GroupView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.GroupQuery)
    @blp.arguments(GeneralParam, location="query", as_kwargs=True)
    @blp.response(200, schemas.GroupPageSchema)
    @paginate()
    def get(self, **kwargs: Dict[str, Any]) -> "BaseQuery[models.Group]":
        # pylint: disable=unused-argument
        """
        获取所有用户组信息——分页
        """
        query = models.Group.where(**kwargs)

        return query

    @doc_login_required
    @permission_required(PERMISSIONS.GroupAdd)
    @blp.arguments(schemas.GroupSchema)
    @blp.response(200, schemas.GroupItemSchema)
    def post(self, group: models.Group) -> Dict[str, models.Group]:
        # pylint: disable=unused-argument
        """
        新增用户组信息
        """
        group.save()
        logger.info(f"{current_user.username}新增了用户组{group}")
        db.session.commit()

        return {"data": group}


@blp.route(
    "/<int:group_id>",
    parameters=[{"in": "path", "name": "group_id", "description": "用户组id"}],
)
class GroupItemView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.GroupEdit)
    @blp.arguments(schemas.GroupSchema)
    @blp.response(200, schemas.GroupItemSchema)
    def put(self, group: models.Group, group_id: int) -> Dict[str, models.Group]:
        """
        更新用户组
        """

        samanager.pk_with(models.Group, group_id)
        group = samanager.update_with(group, commit=False)
        parse_group_change(group)
        db.session.commit()
        logger.info(f"{current_user.username}更新了用户组{group.id_}")

        return {"data": group}

    @doc_login_required
    @permission_required(PERMISSIONS.GroupDelete)
    @blp.response(200, BaseMsgSchema)
    def delete(self, group_id: int) -> None:
        """
        删除用户组
        """
        group = models.Group.find_or_fail(group_id)
        group.roles = []
        parse_group_change(group)
        group.users = []
        group.delete()
        db.session.commit()
        logger.info(f"{current_user.username}删除了用户组{group_id}")

    @doc_login_required
    @permission_required(PERMISSIONS.GroupQuery)
    @blp.response(200, schemas.GroupItemSchema)
    def get(self, group_id: int) -> Dict[str, models.Group]:
        # pylint: disable=unused-argument
        """
        获取单条用户组
        """
        group = models.Group.find_or_fail(group_id)

        return {"data": group}


@blp.route(
    "/<int:group_id>/users",
    parameters=[{"in": "path", "name": "group_id", "description": "用户组id"}],
)
class GroupUserView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.GroupEdit)
    @blp.arguments(schemas.GroupUserSchema)
    @blp.response(200, schemas.GroupItemSchema)
    def put(self, group: models.Group, group_id: int) -> Dict[str, models.Group]:
        """
        更新用户组成员
        """
        samanager.pk_with(models.Group, group_id)
        group = samanager.update_with(group, schemas.GroupUserSchema, commit=False)
        parse_group_users_change(group)
        db.session.commit()
        logger.info(f"{current_user.username}更新了用户组{group.id_}")

        return {"data": group}
