#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SQL语句Builder

    渲染表格模块
"""
from abc import ABC, abstractmethod
from typing import Any, List

from tabulate import tabulate


class TableRender(ABC):
    """
    生成渲染表模块

    通过tabulate生成表格
    get_keys获取键名, parse_records获取表格内容
    """

    @abstractmethod
    def get_keys(self) -> Any:
        """获取所有键"""
        raise NotImplementedError

    @abstractmethod
    def parse_records(self, records: List[Any]) -> Any:
        """处理结果"""
        raise NotImplementedError

    def _render_data_table(self, records: List[Any]) -> str:
        headers = self.get_keys()
        records = self.parse_records(records)  # type: ignore
        return tabulate(records, headers=headers, tablefmt="fancy_grid")
