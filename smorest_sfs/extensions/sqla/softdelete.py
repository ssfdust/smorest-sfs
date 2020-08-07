"""
    smorest_sfs.extensions.sqla.softdelete
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    软删除模块
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, TypeVar

from flask_sqlalchemy import BaseQuery as _BaseQuery
from sqlalchemy.orm import class_mapper

from smorest_sfs.utils.typing import create_fake_generic

M = TypeVar("M")

if TYPE_CHECKING:
    BaseQuery = _BaseQuery
else:
    BaseQuery = create_fake_generic(_BaseQuery)


class QueryWithSoftDelete(BaseQuery[M]):
    """
    软删除模块

    根据deleted字段来决定是否显示此对象
    """

    _with_deleted = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "QueryWithSoftDelete[M]":
        obj: "QueryWithSoftDelete[M]" = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop("_with_deleted", False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    def with_deleted(self) -> "QueryWithSoftDelete[M]":
        return self.__class__(
            class_mapper(self._mapper_zero().class_),  # type: ignore
            session=self.session,
            _with_deleted=True,
        )

    def _get(self, ident: Any) -> Optional[M]:
        """提供原本的get方法"""
        return super(QueryWithSoftDelete, self).get(ident)

    def get(self, ident: Any) -> Optional[M]:
        obj = self.with_deleted()._get(ident)
        deleted = getattr(obj, "deleted", False)
        return obj if obj is None or self._with_deleted or not deleted else None
