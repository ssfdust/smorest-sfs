"""
    SQL语句Builder

    query模块
"""

from abc import abstractmethod
from typing import Any

from flask_sqlalchemy import BaseQuery
from loguru import logger

from .helpers import QueryAnalysis
from .statement import SAStatement


class SAQuery(SAStatement):
    """用于Query的辅助模块"""

    query: BaseQuery

    @abstractmethod
    def get_record(self) -> Any:
        raise NotImplementedError

    def get_sa_sql(self) -> Any:
        return self.query.statement

    def get_keys(self) -> Any:
        analysis = QueryAnalysis(self.query)
        return analysis.keys

    def get_render_sql(self, size: int = 50) -> Any:
        return self.query.limit(size)

    def render_results(self, size: int = 50) -> None:
        query = self.get_render_sql(size)
        analysis = QueryAnalysis(query)
        self.parse_records = lambda x: [analysis.getter(r) for r in x]  # type: ignore
        records = query.all()
        table_data = self._render_data_table(records)
        logger.debug("\n" + table_data)
