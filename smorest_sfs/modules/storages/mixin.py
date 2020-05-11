#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    smorest_sfs.modules.storages.mixin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    文件Mixin处理模块
"""
from typing import IO, Optional

from smorest_sfs.extensions import db
from smorest_sfs.utils.storages import (
    FileStorage,
    load_storage_from_path,
    save_storage_to_path,
)


class StoragesMixin:
    """文件类型Mixin

    支持文件读写以及流操作
    """

    filename: str
    name = db.Column(db.String(256), nullable=True, doc="文件名")
    filetype = db.Column(db.String(256), nullable=False, doc="文件类型", default="")
    storetype = db.Column(db.String(256), nullable=False, doc="存储类型")
    saved = db.Column(db.Boolean, nullable=True, default=False, doc="是否保存")
    path = db.Column(db.String(2000), nullable=True, doc="文件路径")
    _store: FileStorage

    @property
    def store(self) -> FileStorage:
        """返回文件的FileStorage对象"""
        if self.saved and not hasattr(self, "_store"):
            self._store = load_storage_from_path(self.name, self.path)
        elif not hasattr(self, "_store") and not self.saved:
            raise FileExistsError
        return self._store

    @store.setter
    def store(self, val: Optional[FileStorage]) -> None:
        if val:
            self._store = val

    def as_stream(self) -> IO[bytes]:
        # pylint: disable=C0116
        try:
            self.store.stream.seek(0)
        except ValueError:
            delattr(self, "_store")
        return self.store.stream

    def save_store(self) -> None:
        """
        存储文件

        每一次存储文件都会生成一个新的地址
        """
        if self.store:
            self.name = self.store.filename if self.store.filename else self.filename
            self.filetype = self.store.content_type or "application/octstream"
            self.path = save_storage_to_path(self.store, self.storetype)
            self.saved = True
