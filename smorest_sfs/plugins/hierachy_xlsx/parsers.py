#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from typing import Any, Dict, List, Optional, Protocol

from pyexcel import get_book
from pyexcel.book import Book
from pyexcel.sheet import Sheet

from smorest_sfs.utils.text import camel_to_snake

IDENT_KEY = "<IDENT>"
NAME_KEY = "name"


class IOProtocol(Protocol):
    def read(self) -> bytes:  # pragma: no cover
        ...


class _HierachyParser:
    """
    将文件行转为文件列

    关系表：表格名称为`Relations`的表格，用一个类似展开的方式描述
    等级关系。
    例如：
    A | B  | C
    B | B1 | C1
    C |    | C2

    表示：A、B、C为父级，B1为B的子级，C1，C2为C的子级，A没有子级。

    属性表：表格名为`Attrs`的表格，用类似数据库表的形式表示一个对象
    的属性。
    例如：
    Name |    Date    | Action
      A  | 2020-07-18 |  Read
      B  | 2020-07-18 |  Write
      C  | 2020-07-18 |  Read
      B1 | 2020-07-18 |  Write
      C1 | 2020-07-18 |  Read
      C2 | 2020-07-18 |  Write

    将两张表格联系起来，就可以得到完整的树型结构信息。
    """

    def __init__(
        self, stream: Optional[IOProtocol] = None,
    ):
        """初始化

        Attributes:
            mapping: 主键与名字的对应关系
            ident: 主键名称
            title_list: 表栏目名称
            relation_list: 关系名称
        """
        self.workbook: Book = get_book(file_stream=stream, file_type="xlsx")
        self._sheet_names: List[str] = self.workbook.sheet_names()
        self.mapping: Dict[str, Any] = {}
        self.ident: Optional[str] = None
        self.title_list: List[str] = []
        self.relation_list: List[List[Any]] = []

        self.relation_sheet: Sheet
        self.attr_sheet: Sheet

    def _load_workbook(self) -> None:
        """加载关系表以及属性表"""
        self.relation_sheet = self.workbook["Relations"]
        self.attr_sheet = self.workbook["Attrs"]
        self.attr_sheet.name_columns_by_row(0)


class _AttrParser(_HierachyParser):
    def _parse_attr_worksheet(self) -> None:
        self._get_title_list_and_ident()
        self._parse_attrs()

    def _parse_attrs(self) -> None:
        """过滤主键为空的行，并以主键为标记加入到mapping"""
        if self.ident:
            self.attr_sheet.colnames = self.title_list
            for item in filter(itemgetter(self.ident), self.attr_sheet.to_records()):
                self.mapping[item[self.ident]] = item

    def _get_title_list_and_ident(self) -> None:
        """获取下划线形式的表成员"""
        self.title_list = list(map(camel_to_snake, self.attr_sheet.colnames))
        if len(self.title_list) > 0:
            self.ident = self.title_list[0]
        else:
            raise ValueError("The excel column name row must be longer than zero.")


class HierachyParser(_AttrParser):
    def _parse_worksheet(self) -> None:
        self._parse_attr_worksheet()
        self._parse_relation_worksheet()

    def parse(self) -> None:
        self._load_workbook()
        self._parse_worksheet()

    def _parse_relation_worksheet(self) -> None:
        relation: Sheet = self.relation_sheet.clone()
        relation.transpose()
        self.relation_list = [
            [key for key in filter(any, cols)] for cols in relation.to_array()
        ]
