"""
    smorest_sfs.modules.codes.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    编码的资源模块
"""
from typing import Any, Dict

from flask.views import MethodView

from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.auth.decorators import doc_login_required, permission_required

from . import blp, models, schemas


@blp.route("/options")
class CodeListView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.CodeQuery)
    @blp.arguments(schemas.TypeCodeSchema, location="query", as_kwargs=True)
    @blp.response(schemas.CodeListSchema)
    def get(self, type_code: str) -> Dict[str, Any]:
        # pylint: disable=unused-argument
        """
        获取所有编码选项信息
        """
        schema = schemas.CodeOptsSchema()
        codes = models.Code.get_tree(
            models.db.session,
            json=True,
            json_fields=schema.dump,
            query=lambda q: q.filter_by(type_code=type_code),
        )

        return {"data": codes}
