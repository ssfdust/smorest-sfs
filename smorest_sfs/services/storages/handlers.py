"""
    smorest_sfs.services.storages.handlers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    文件处理工厂
"""
from typing import Any

from werkzeug.datastructures import FileStorage

from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.utils.storages import delete_from_rel_path


class StorageFactory:
    """文件处理

    文件的CRUD操作
    """

    def __init__(self, storage: Storages):
        self.storage = storage

    def save(self, commit: bool = True) -> Storages:
        """文件保存"""
        self.storage.save_store()
        return self.storage.save()  # type: ignore

    def update(self, store: FileStorage, **kwargs: Any) -> Storages:
        """文件更新"""
        self.storage.store = store
        self.storage.save_store()
        return self.storage.update(**kwargs)  # type: ignore

    def hard_delete(self, commit: bool = True) -> None:
        """文件永久删除"""
        if self.storage.path:
            delete_from_rel_path(self.storage.path)
            self.storage.deleted = True
            self.storage.saved = False
            Storages.query.filter_by(id_=self.storage.id_).delete()
