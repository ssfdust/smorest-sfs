#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SQL语句Builder

    abc模块
"""

from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, Type, TypeVar

import pyperclip
import sqlparse
from loguru import logger
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.orm import Session
from tabulate import tabulate

_S = TypeVar("_S")
_R = TypeVar("_R")
_T = TypeVar("_T")


class TableRenderABC(ABC, Generic[_S, _R, _T]):
    """生成渲染表模块

    生成表格字符串，提供打印表格函数
    """

    @abstractmethod
    def get_render_records(self, size: int = 50) -> List[Dict[str, str]]:
        """处理结果"""
        raise NotImplementedError

    def _render_data_table(self, size: int = 50) -> str:
        """渲染表格字符串"""
        records = self.get_render_records(size)
        return tabulate(records, headers="keys", tablefmt="fancy_grid")

    def render_results(self, size: int = 50) -> None:
        """渲染指定长度的表格结果并debug出来"""
        table_data = self._render_data_table()
        logger.debug(f"\n{table_data}")


class StatementABC(ABC, Generic[_S, _R, _T]):
    """Statement的抽象类

    提供获取sql字符串的方法，并提供打印与复制sql的函数
    """

    _DIALECT: Type[DefaultDialect]
    _session: Session

    @abstractmethod
    def sa_sql(self) -> _S:
        """获取sa_sql的abc方法"""
        raise NotImplementedError

    def raw_sql(self) -> str:
        """根据DIALECT获取原始sql字符串"""
        sa_sql = self.sa_sql()
        compiled_sql = sa_sql.compile(  # type: ignore
            dialect=self._DIALECT(), compile_kwargs={"literal_binds": True},
        )

        formated_sql: str = sqlparse.format(
            str(compiled_sql), reindent=True, reindent_aligned=False, indent_width=4
        )
        return formated_sql

    def debug_sql(self, need_copy: bool = True) -> None:
        """打印sql并复制sql到剪切板"""
        raw_sql = self.raw_sql()
        logger.debug("\n" + raw_sql)
        if need_copy:
            pyperclip.copy(raw_sql)


class RenderableStatementABC(StatementABC[_S, _R, _T], TableRenderABC[_S, _R, _T]):
    """渲染模块"""

    @classmethod
    def init_statement(cls, session: Session, dialect: Type[DefaultDialect]) -> None:
        cls._DIALECT = dialect
        cls._session = session

    @abstractmethod
    def first(self) -> Optional[_R]:
        ...

    @abstractmethod
    def all(self) -> List[_R]:
        ...

    @abstractmethod
    def scalar(self) -> Optional[_T]:
        ...
