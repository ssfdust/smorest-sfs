"""
    smorest_sfs.modules.menus.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    菜单的资源模块
"""
from typing import Any, Dict

from flask.views import MethodView

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.auth.decorators import doc_login_required, role_required

from . import blp, models, schemas


@blp.route("")
class MenuView(MethodView):
    @doc_login_required
    @role_required(ROLES.User)
    @blp.response(schemas.MenuListSchema)
    def get(self) -> Dict[str, Any]:
        # pylint: disable=unused-argument
        """
        获取所有菜单信息——分页
        """
        schema = schemas.MenuOptsSchema()
        data = models.Menu.get_tree(
            session=models.db.session,
            json=True,
            json_fields=schema.dump,
            query=models.menu_filter,
        )

        return {"data": data}
