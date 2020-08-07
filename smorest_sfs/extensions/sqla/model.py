#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    smorest_sfs.extensions.sqla.model
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    自定义Model模块
"""
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy_mixins.activerecord import ActiveRecordMixin
from sqlalchemy_mixins.repr import ReprMixin
from sqlalchemy_mixins.smartquery import SmartQueryMixin

from .softdelete import QueryWithSoftDelete

M = TypeVar("M", bound="Model")

DELETED_KEY = "deleted"


class Model(ActiveRecordMixin, SmartQueryMixin, ReprMixin):
    """简单的CRUD处理"""

    __abstract__ = True

    query_class = QueryWithSoftDelete[M]

    def delete(self) -> None:
        setattr(self, DELETED_KEY, True)
        self.save()

    @classmethod
    def id_in(cls, ids: List[int]) -> QueryWithSoftDelete[M]:
        return cls.query.filter(cls.id_.in_(ids))

    @classmethod
    def destroy(cls, *ids: Any) -> None:
        cls.session.bulk_update_mappings(
            cls, [{"deleted": True, "id_": id_} for id_ in ids]
        )

    @classmethod
    def smart_query(
        cls: Type[M],
        filters: Optional[Dict[str, Any]] = None,
        sort_attrs: Optional[Any] = None,
        schema: Optional[Any] = None,
    ) -> QueryWithSoftDelete[M]:
        return super().smart_query(filters, sort_attrs, schema)  # type: ignore

    @classmethod
    def where(cls: Type[M], **filters: Any) -> QueryWithSoftDelete[M]:
        return super().where(**filters)  # type: ignore
