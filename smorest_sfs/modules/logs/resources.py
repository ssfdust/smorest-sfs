"""
    smorest_sfs.modules.logs.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    日志的资源模块
"""
from typing import Any

from flask.views import MethodView
from flask_sqlalchemy import BaseQuery

from smorest_sfs.extensions.api.decorators import paginate
from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.auth.decorators import doc_login_required, permission_required

from . import blp, models, schemas


@blp.route("/log-details")
class LogView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.LogQuery)
    @blp.arguments(schemas.LogParam, location="query", as_kwargs=True)
    @blp.response(200, schemas.LogPageSchema)
    @paginate()
    def get(self, **kwargs: Any) -> "BaseQuery[models.Log]":
        # pylint: disable=unused-argument
        """
        获取所有日志信息——分页
        """
        query = models.Log.where(**kwargs).order_by(models.Log.id_.desc())

        return query


@blp.route("/responselog-details")
class ResponseLogView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.LogQuery)
    @blp.arguments(schemas.RespLogParam, location="query", as_kwargs=True)
    @blp.response(200, schemas.RespLogPageSchema)
    @paginate()
    def get(self, **kwargs: Any) -> "BaseQuery[models.Log]":
        # pylint: disable=unused-argument
        """
        获取所有日志信息——分页
        """
        query = models.ResponseLog.where(**kwargs).order_by(
            models.ResponseLog.id_.desc()
        )

        return query
