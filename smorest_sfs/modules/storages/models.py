"""
    smorest_sfs.modules.storages.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    文件管理ORM模块
"""
from typing import Any

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db

from .mixin import StoragesMixin


class Storages(Model, SurrogatePK, StoragesMixin):
    """
    文件管理表

    :attr name: str(256) 文件名
    :attr filetype: str(256) 文件类型
    :attr storetype: str(256) 存储类型
    :attr saved: bool 是否保存
    :attr path: str(2000) 保存路径
    :attr uid: int 用户ID
    :attr _store: FileStorage 文件
    """

    __tablename__ = "storages"

    uid = db.Column(db.Integer, doc="用户ID")

    def __init__(self, **kwargs: Any):
        self.store = kwargs.pop("store")
        super().__init__(**kwargs)
