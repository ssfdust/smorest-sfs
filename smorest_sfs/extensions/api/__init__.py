"""
    smorest_sfs.extensions.api
    ~~~~~~~~~~~~~~~~~~~~
    smorest api配置模块
"""
from typing import Any, Dict, Optional, Tuple

from flask_smorest import Api as BaseApi
from flask_smorest import Blueprint
from sqlalchemy_mixins import ModelNotFoundError

from smorest_sfs.extensions.marshal import UploadField


class Api(BaseApi):  # type: ignore
    """为flask-smorest的API模块提供base_prefix功能"""

    def register_blueprint(
        self, blp: Blueprint, base_prefix: Optional[str] = None, **options: Any
    ) -> None:
        # pylint: disable=W0221
        """注册蓝图

        组合新前缀url与蓝图默认前缀url

        :param base_prefix str: 新的前缀
        :param blp Blueprint: 待注册蓝图
        :param options dict: 蓝图参数

        app初始化后调用
        """
        url_prefix = options.get("url_prefix", blp.url_prefix)
        if base_prefix is not None:
            options["url_prefix"] = base_prefix + url_prefix

        self._app.register_blueprint(blp, **options)

        blp.register_views_in_doc(self, self._app, self.spec)

        self.spec.tag({"name": blp.name, "description": blp.description})

    def _register_error_handlers(self) -> None:
        super()._register_error_handlers()
        self._app.register_error_handler(ModelNotFoundError, self.handle_find_fail)

    def handle_find_fail(self, error: Any) -> Tuple[Dict[str, str], int]:
        return {"message": "asasas"}, 404


spec_kwargs = {
    "components": {
        "securitySchemes": {
            "api_key": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
            "refresh_key": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
        }
    }
}

api = Api(spec_kwargs=spec_kwargs)

api.register_field(UploadField, "string", "binary")
