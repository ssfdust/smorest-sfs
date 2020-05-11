#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试插件中的sa辅助函数
"""
from typing import Callable, Type, TypeVar

import pyperclip
import pytest

from smorest_sfs.extensions.sqla import Model
from smorest_sfs.plugins.sa import SAQuery, debug_sql, execute, render_limit_results
from smorest_sfs.plugins.sa.statement import SAStatement
from tests._utils.uniqueue import UniqueQueue
from tests.extensions.sqla.test_sqla import ItemsFixtureBase

T = TypeVar("T")


class TestSASql(ItemsFixtureBase):
    fixture_names = ("TestCRUDTable", "TestSASql")
    TestSASql: Type[SAStatement]
    raw_sql = (
        "SELECT sqla_test_crud_table.name\n"
        "FROM sqla_test_crud_table\n"
        "WHERE sqla_test_crud_table.name = '{name}'"
    )
    table_str = "╒════════╕\n" "│ name   │\n" "╞════════╡\n" "│ bbc    │\n" "╘════════╛"

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items")
    @pytest.mark.parametrize("name, count", [("bbc", 1), ("aac", 0)])
    def test_sql_could_run(self, name: str, count: int) -> None:
        data = execute(self.TestSASql, name=name)
        assert len(data) == count

    @pytest.mark.parametrize("name", ["bbc", "aac"])
    def test_raw_sql_should_rendered(self, name: str) -> None:
        test_sql = self.TestSASql(name)
        assert test_sql.get_raw_sql() == self.raw_sql.format(name=name)

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items", "inject_logger")
    def test_table_should_rendered(self) -> None:
        render_limit_results(self.TestSASql, "bbc")
        assert self._get_debug() == "\n" + self.table_str

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items", "inject_logger")
    def test_debug_should_rendered(self) -> None:
        debug_sql(self.TestSASql, "bbc")
        assert pyperclip.paste() == self.raw_sql.format(
            name="bbc"
        ) and self._get_debug() == "\n" + self.raw_sql.format(name="bbc")

    def _get_debug(self) -> str:
        queue: UniqueQueue[str] = UniqueQueue()
        record: str = queue.get(timeout=1)
        return record


class TestSAPlugin(ItemsFixtureBase):
    fixture_names = (
        "TestCRUDTable",
        "TestSASql",
        "TestChildTable",
        "TestOneTableQuery",
        "TestOneColQuery",
        "TestTwoTablesQuery",
    )
    TestCRUDTable: Type[Model]
    TestSASql: Type[SAStatement]
    TestChildTable: Type[Model]
    TestOneColQuery: Type[SAQuery]
    TestTwoTablesQuery: Type[SAQuery]

    @pytest.mark.usefixtures(
        "TestTableTeardown", "crud_items", "child_items", "inject_logger"
    )
    @pytest.mark.parametrize(
        "func, sql, result",
        [
            (
                debug_sql,
                "TestOneColQuery",
                (
                    "\n"
                    "SELECT sqla_test_crud_table.name\n"
                    "FROM sqla_test_crud_table\n"
                    "WHERE sqla_test_crud_table.name = 'bbc'"
                ),
            ),
            (
                render_limit_results,
                "TestOneColQuery",
                ("\n╒════════╕\n│ name   │\n╞════════╡\n│ bbc    │\n╘════════╛"),
            ),
            (
                debug_sql,
                "TestOneTableQuery",
                (
                    "\n"
                    "SELECT sqla_test_crud_table.id,\n"
                    "       sqla_test_crud_table.deleted,\n"
                    "       sqla_test_crud_table.modified,\n"
                    "       sqla_test_crud_table.created,\n"
                    "       sqla_test_crud_table.name\n"
                    "FROM sqla_test_crud_table\n"
                    "WHERE sqla_test_crud_table.deleted = false\n"
                    "    AND sqla_test_crud_table.name = 'bbc'"
                ),
            ),
            (
                render_limit_results,
                "TestOneTableQuery",
                (
                    "\n"
                    "╒══════╤═══════════╤══════════════════════════"
                    "═╤═══════════════════════════╤════════╕\n"
                    "│   id │ deleted   │ modified                 "
                    " │ created                   │ name   │\n"
                    "╞══════╪═══════════╪══════════════════════════"
                    "═╪═══════════════════════════╪════════╡\n"
                    "│    4 │ False     │ 1994-09-11T08:20:00+00:00"
                    " │ 1994-09-11T08:20:00+00:00 │ bbc    │\n"
                    "╘══════╧═══════════╧══════════════════════════"
                    "═╧═══════════════════════════╧════════╛"
                ),
            ),
            (
                debug_sql,
                "TestTwoTablesQuery",
                (
                    "\n"
                    "SELECT sqla_test_crud_table.id,\n"
                    "       sqla_test_crud_table.deleted,\n"
                    "       sqla_test_crud_table.modified,\n"
                    "       sqla_test_crud_table.created,\n"
                    "       sqla_test_crud_table.name,\n"
                    "       test_crud_child_table.id,\n"
                    "       test_crud_child_table.deleted,\n"
                    "       test_crud_child_table.modified,\n"
                    "       test_crud_child_table.created,\n"
                    "       test_crud_child_table.name,\n"
                    "       test_crud_child_table.pid,\n"
                    "       sqla_test_crud_table.id AS crud_id\n"
                    "FROM sqla_test_crud_table,\n"
                    "     test_crud_child_table\n"
                    "WHERE sqla_test_crud_table.name = 'bbc'"
                ),
            ),
            (
                render_limit_results,
                "TestTwoTablesQuery",
                (
                    "\n"
                    "╒═══════════════════╤═══════════════════"
                    "═╤══════════╤════════╤═══════════╕\n"
                    "│ TestCRUDTable     │ TestChildTable    "
                    " │ name     │ name   │   crud_id │\n"
                    "╞═══════════════════╪═══════════════════"
                    "═╪══════════╪════════╪═══════════╡\n"
                    "│ <TestCRUDTable 4> │ <TestChildTable 1>"
                    " │ aaabbb   │ bbc    │         4 │\n"
                    "├───────────────────┼───────────────────"
                    "─┼──────────┼────────┼───────────┤\n"
                    "│ <TestCRUDTable 4> │ <TestChildTable 2>"
                    " │ bbbbcccc │ bbc    │         4 │\n"
                    "├───────────────────┼───────────────────"
                    "─┼──────────┼────────┼───────────┤\n"
                    "│ <TestCRUDTable 4> │ <TestChildTable 3>"
                    " │ bbcccc   │ bbc    │         4 │\n"
                    "├───────────────────┼───────────────────"
                    "─┼──────────┼────────┼───────────┤\n"
                    "│ <TestCRUDTable 4> │ <TestChildTable 4>"
                    " │ bbc      │ bbc    │         4 │\n"
                    "╘═══════════════════╧═══════════════════"
                    "═╧══════════╧════════╧═══════════╛"
                ),
            ),
        ],
    )
    def test_general_function(
        self, func: Callable[..., None], sql: str, result: str
    ) -> None:
        sql_cls = getattr(self, sql)
        func(sql_cls)
        assert self._get_debug() == result

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items")
    def test_query_could_run(self) -> None:
        data = execute(self.TestOneColQuery)
        assert len(data) > 0

    def _get_debug(self) -> str:
        queue: UniqueQueue[str] = UniqueQueue()
        item = queue.get(timeout=1)
        queue.empty()
        return item
