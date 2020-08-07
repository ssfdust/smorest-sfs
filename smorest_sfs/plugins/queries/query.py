"""
    SQL语句Builder

    query模块
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Query

from .abstract import _R, _S, _T, RenderableStatementABC


class SAQuery(RenderableStatementABC[_S, _R, _T]):
    """用于Query的辅助模块"""

    _query: "Query[_R]"

    def __init__(self, *args: Any, **kwargs: Any):
        ...

    def get_render_records(self, size: int = 50) -> List[Dict[str, str]]:
        query = self.query()
        results: List[Dict[str, str]] = []
        for record in query.limit(size).only_return_tuples(True).all():  # type: ignore
            results.append({key: str(getattr(record, key)) for key in record.keys()})
        return results

    def sa_sql(self) -> _S:
        statement: _S = self._query.statement
        return statement

    def query(self) -> "Query[_R]":
        return self._query

    def first(self) -> Optional[_R]:
        return self._query.first()

    def all(self) -> List[_R]:
        return self._query.all()

    def scalar(self) -> Optional[_T]:
        item: Optional[_T] = self._query.scalar()
        return item
