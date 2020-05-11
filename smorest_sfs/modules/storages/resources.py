"""
    smorest_sfs.modules.storages.resources
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from typing import Any, Dict, Union

from flask.views import MethodView
from loguru import logger

from smorest_sfs.extensions.marshal.bases import BaseMsgSchema
from smorest_sfs.modules.auth import PERMISSIONS, ROLES
from smorest_sfs.modules.auth.decorators import (
    doc_login_required,
    permission_required,
    role_required,
)
from smorest_sfs.services.storages.handlers import StorageFactory
from smorest_sfs.utils.storages import FileStorage, Response, make_response_from_store

from . import blp, models, schemas


@blp.route("/<int:file_id>")
class StoragesView(MethodView):
    """
    文件CRUD视图
    """

    @doc_login_required
    @role_required(ROLES.User)
    @blp.response(code=200, description="获取文件")
    def get(self, file_id: int) -> Response:
        """
        获取文件
        """
        storage = models.Storages.get_by_id(file_id)

        return make_response_from_store(storage.store)

    @doc_login_required
    @role_required(ROLES.User)
    @blp.arguments(schemas.UploadParams(), location="files")
    @blp.response(BaseMsgSchema)
    def put(
        self, args: Dict[str, FileStorage], file_id: int
    ) -> Dict[str, Union[int, str]]:
        """
        修改文件
        """
        args["store"] = args.pop("file")
        storage = models.Storages.get_by_id(file_id)
        factory = StorageFactory(storage)
        logger.info(f"修改了文件{storage.name} id: {storage.id}")
        factory.update(commit=True, **args)

        return {"code": 0, "msg": "success"}

    @doc_login_required
    @role_required(ROLES.User)
    @blp.response(BaseMsgSchema)
    def delete(self, file_id: int) -> None:
        """
        删除文件
        """
        storage = models.Storages.get_by_id(file_id)
        logger.info(f"删除了文件{storage.name} id: {storage.id}")
        storage.delete()


@blp.route("/force/delete/<int:file_id>")
class ForceDeleteView(MethodView):
    """永久删除文件视图"""

    @doc_login_required
    @permission_required(PERMISSIONS.FileForceDelete)
    @blp.response(BaseMsgSchema)
    def delete(self, file_id: int) -> Dict[str, Any]:
        """永久删除文件"""
        storage = models.Storages.get_by_id(file_id)
        factory = StorageFactory(storage)
        factory.hard_delete()

        return {"code": 0, "msg": "success"}


@blp.route("/upload/<storetype>")
class UploadView(MethodView):
    """上传管理视图"""

    @doc_login_required
    @role_required(ROLES.User)
    @blp.arguments(schemas.UploadParams(), location="files")
    @blp.response(schemas.UploadSchema)
    def post(
        self, args: Dict[str, FileStorage], storetype: str
    ) -> Dict[str, Union[int, str, Dict[str, int]]]:
        """
        上传文件
        """
        logger.info(f"上传了文件{args['file'].filename}")
        args["store"] = args.pop("file")
        factory = StorageFactory(models.Storages(storetype=storetype, **args))
        factory.save()

        return {"code": 0, "msg": "success", "data": {"file_id": factory.storage.id}}
