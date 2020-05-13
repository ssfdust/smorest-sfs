"""
    smorest_sfs.modules.projects.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    项目的资源模块
"""
from typing import Any, Dict, List

from flask.views import MethodView
from flask_sqlalchemy import BaseQuery
from loguru import logger

from flask_jwt_extended import current_user
from smorest_sfs.extensions.api.decorators import paginate
from smorest_sfs.extensions.marshal.bases import (BaseIntListSchema,
                                                  BaseMsgSchema,
                                                  GeneralParam)
from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.auth.decorators import (doc_login_required,
                                                 permission_required)

from . import blp, models, schemas


@blp.route('/options')
class ProjectListView(MethodView):

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectQuery)
    @blp.response(schemas.ProjectListSchema)
    def get(self) -> Dict[str, List[models.Project]]:
        # pylint: disable=unused-argument
        '''
        获取所有项目选项信息
        '''
        query = models.Project.query

        items = query.all()

        return {'data': items}


@blp.route('')
class ProjectView(MethodView):

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectQuery)
    @blp.arguments(GeneralParam, location="query", as_kwargs=True)
    @blp.response(schemas.ProjectPageSchema)
    @paginate()
    def get(self, **kwargs: Dict[str, Any]) -> BaseQuery:
        # pylint: disable=unused-argument
        '''
        获取所有项目信息——分页
        '''
        query = models.Project.where(**kwargs)

        return query

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectAdd)
    @blp.arguments(schemas.ProjectSchema)
    @blp.response(schemas.ProjectItemSchema)
    def post(self, project: models.Project) -> Dict[str, models.Project]:
        # pylint: disable=unused-argument
        '''
        新增项目信息
        '''
        project.save()
        logger.info(f"{current_user.username}新增了项目{project}")

        return {'data': project}

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectDelete)
    @blp.arguments(BaseIntListSchema, as_kwargs=True)
    @blp.response(BaseMsgSchema)
    def delete(self, lst: List[int]) -> None:
        # pylint: disable=unused-argument
        '''
        批量删除项目
        -------------------------------
        :param lst: list 包含id列表的字典
        '''

        models.Project.delete_by_ids(lst)
        logger.info(f"{current_user.username}删除了项目{lst}")


@blp.route('/<int:project_id>',
           parameters=[
               {'in': 'path', 'name': 'project_id', 'description': '项目id'}
           ])
class ProjectItemView(MethodView):

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectEdit)
    @blp.arguments(schemas.ProjectSchema)
    @blp.response(schemas.ProjectItemSchema)
    def put(self, project: models.Project, project_id: int) -> Dict[str, models.Project]:
        '''
        更新项目
        '''

        project = models.Project.update_by_id(project_id,
                                                                        schemas.ProjectSchema,
                                                                        project)
        logger.info(f"{current_user.username}更新了项目{project.id}")

        return {'data': project}

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectDelete)
    @blp.response(BaseMsgSchema)
    def delete(self, project_id: int) -> None:
        '''
        删除项目
        '''
        models.Project.delete_by_id(project_id)
        logger.info(f"{current_user.username}删除了项目{project_id}")

    @doc_login_required
    @permission_required(PERMISSIONS.ProjectQuery)
    @blp.response(schemas.ProjectItemSchema)
    def get(self, project_id: int) -> Dict[str, models.Project]:
        # pylint: disable=unused-argument
        '''
        获取单条项目
        '''
        project = models.Project.get_by_id(project_id)

        return {'data': project}