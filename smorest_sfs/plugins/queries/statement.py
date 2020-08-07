"""
    SQL语句Builder

    sa raw sql模块
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.engine import ResultProxy, RowProxy
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.sql import Select

from .abstract import _S, _T, RenderableStatementABC


class SAStatement(RenderableStatementABC[_S, RowProxy, _T]):
    _sa_sql: _S

    def __init__(self, *args: Any, **kwargs: Any):
        ...

    def sa_sql(self) -> _S:
        return self._sa_sql

    def get_render_records(self, size: int = 50) -> List[Dict[str, str]]:
        sa_sql = self.sa_sql()
        assert isinstance(sa_sql, Select)
        render_sql = sa_sql.limit(size)
        cursor = self._session.execute(render_sql)
        records = cursor.fetchall()
        return [{str(k): str(v) for k, v in record.items()} for record in records]

    @property
    def _executor(self) -> ResultProxy:
        cursor: ResultProxy = self._session.execute(self._sa_sql)
        return cursor

    def first(self) -> Optional[RowProxy]:
        try:
            return self._executor.first()
        except ResourceClosedError:
            return None

    def all(self) -> List[RowProxy]:
        try:
            return self._executor.fetchall()
        except ResourceClosedError:
            return []

    def scalar(self) -> Optional[_T]:
        try:
            item: Optional[_T] = self._executor.scalar()
            return item
        except ResourceClosedError:
            return None
