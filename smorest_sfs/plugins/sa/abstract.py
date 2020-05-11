#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SQL语句Builder

    abc模块
"""

from abc import ABC, abstractmethod
from typing import Any, List, Union

import pyperclip
import sqlparse
from loguru import logger
from sqlalchemy.dialects import postgresql
from sqlalchemy import delete, insert, select, update

from .render import TableRender


class StatementAbstract(ABC):
    """Statement的抽象类"""

    @abstractmethod
    def get_sa_sql(self) -> Union[select, insert, update, delete]:
        """获取sa_sql的abc方法"""
        raise NotImplementedError

    def get_raw_sql(self) -> str:
        """获取原始sql字符串的abc方法"""
        sa_sql = self.get_sa_sql()
        compiled_sql = sa_sql.compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True},
        )
        _raw_sql = str(compiled_sql)
        return sqlparse.format(
            _raw_sql, reindent=True, reindent_aligned=False, indent_width=4
        )

    def debug_sql(self, need_copy: bool = True) -> None:
        """debug sql的abc方法"""
        raw_sql = self.get_raw_sql()
        logger.debug("\n" + raw_sql)
        if need_copy:
            pyperclip.copy(raw_sql)


class RenderableStatement(StatementAbstract, TableRender):
    """渲染模块"""

    @abstractmethod
    def get_sa_sql(self) -> Union[select, insert, update, delete]:
        """获取sa_sql的abc方法"""
        raise NotImplementedError

    @abstractmethod
    def get_keys(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_render_sql(self, size: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def parse_records(self, records: List[Any]) -> Any:  # type: ignore
        raise NotImplementedError
