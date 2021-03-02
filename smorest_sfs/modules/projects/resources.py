"""
    smorest_sfs.modules.projects.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    项目的资源模块
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

from smorest_sfs.modules.projects.models import Project
from smorest_sfs.plugins.samanager import SqlaManager

from . import blp, models, schemas

samanager: SqlaManager[Project] = SqlaManager(db.session)


@blp.route("/options")
class ProjectListView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.ProjectQuery)
    @blp.response(200, schemas.ProjectListSchema)
    def get(self) -> Dict[str, List[Project]]:
        # pylint: disable=unused-argument
        """
        获取所有项目选项信息
        """
        query = Project.query

        items = query.all()

        return {"data": items}


@blp.route("")
class ProjectView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.ProjectQuery)
    @blp.arguments(GeneralParam, location="query", as_kwargs=True)
    @blp.response(200, schemas.ProjectPageSchema)
    @paginate()
    def get(self, **kwargs: Dict[str, Any]) -> "BaseQuery[Project]":
        # pylint: disable=unused-argument
        """
        获取所有项目信息——分页
        """
        query = Project.where(**kwargs)

        return query

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectAdd)
    @blp.arguments(schemas.ProjectSchema)
    @blp.response(200, schemas.ProjectItemSchema)
    def post(self, project: Project) -> Dict[str, Project]:
        # pylint: disable=unused-argument
        """
        新增项目信息
        """
        project.save()
        logger.info(f"{current_user.username}新增了项目{project}")
        db.session.commit()

        return {"data": project}

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectDelete)
    @blp.arguments(BaseIntListSchema, as_kwargs=False)
    @blp.response(200, BaseMsgSchema)
    def delete(self, lst: Dict[str, List[int]]) -> None:
        # pylint: disable=unused-argument
        """
        批量删除项目
        -------------------------------
        :param lst: list 包含id列表的字典
        """

        models.Project.destroy(*lst["lst"])
        logger.info(f"{current_user.username}删除了项目{lst}")
        db.session.commit()


@blp.route(
    "/<int:project_id>",
    parameters=[{"in": "path", "name": "project_id", "description": "项目id"}],
)
class ProjectItemView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.ProjectEdit)
    @blp.arguments(schemas.ProjectSchema)
    @blp.response(200, schemas.ProjectItemSchema)
    def put(
        self, project: models.Project, project_id: int
    ) -> Dict[str, models.Project]:
        """
        更新项目
        """
        samanager.pk_with(Project, project_id)
        project = samanager.update_with(project)
        logger.info(f"{current_user.username}更新了项目{project.id_}")
        db.session.commit()

        return {"data": project}

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectDelete)
    @blp.response(200, BaseMsgSchema)
    def delete(self, project_id: int) -> None:
        """
        删除项目
        """
        Project.destroy(project_id)
        logger.info(f"{current_user.username}删除了项目{project_id}")
        db.session.commit()

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectQuery)
    @blp.response(200, schemas.ProjectItemSchema)
    def get(self, project_id: int) -> Dict[str, models.Project]:
        # pylint: disable=unused-argument
        """
        获取单条项目
        """
        project = models.Project.find_or_fail(project_id)

        return {"data": project}
