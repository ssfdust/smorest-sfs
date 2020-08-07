from typing import TYPE_CHECKING, Type, TypeVar

import pytest
from sqlalchemy.sql import Select

from smorest_sfs.plugins.queries import (
    SAStatement,
    debug_sql,
    execute,
    quick_render,
    render_limit_results,
)
from tests._utils.uniqueue import UniqueQueue

_T = TypeVar("_T")
_S = TypeVar("_S")
queue: UniqueQueue[str] = UniqueQueue()

if TYPE_CHECKING:
    from .models import User


@pytest.mark.parametrize(
    "sql, res_txt",
    (
        (1, ["sqls", 1]),
        (2, ["sqls", 2]),
        (3, ["sqls", 3]),
        (4, ["sqls", 4]),
        (5, ["sqls", 5]),
    ),
    indirect=True,
)
@pytest.mark.usefixtures("inject_logger")
def test_debug_sql(sql: Type[SAStatement[_S, _T]], res_txt: str) -> None:
    debug_sql(sql)
    assert queue.get().strip() == res_txt


@pytest.mark.parametrize(
    "sql, res_txt", ((1, ["sql_tables", 1]), (2, ["sql_tables", 2]),), indirect=True,
)
@pytest.mark.usefixtures("inject_logger")
def test_render_sql(sql: Type[SAStatement[_S, _T]], res_txt: str) -> None:
    render_limit_results(sql)
    assert queue.get().strip() == res_txt


@pytest.mark.parametrize("sql", (1, 2, 3, 4, 5), indirect=True)
@pytest.mark.parametrize("method", ["first", "all", "scalar"])
@pytest.mark.usefixtures("delete_items")
def test_execute_statement(sql: Type[SAStatement[_S, _T]], method: str) -> None:
    res = execute(sql, method)  # type: ignore
    sa_sql = sql().sa_sql()
    if not isinstance(sa_sql, Select):
        assert not res
    else:
        assert res


@pytest.mark.usefixtures("inject_logger")
def test_quick_render(UserModel: Type["User"]) -> None:
    quick_render(UserModel.__table__)
    res_txt = (
        "╒══════╤════════╤════════════╕\n"
        "│   id │ name   │ nickname   │\n"
        "╞══════╪════════╪════════════╡\n"
        "│    1 │ name0  │ nickname0  │\n"
        "├──────┼────────┼────────────┤\n"
        "│    2 │ name1  │ nickname1  │\n"
        "├──────┼────────┼────────────┤\n"
        "│    3 │ name2  │ nickname2  │\n"
        "├──────┼────────┼────────────┤\n"
        "│    4 │ name3  │ nickname3  │\n"
        "├──────┼────────┼────────────┤\n"
        "│    5 │ name4  │ nickname4  │\n"
        "╘══════╧════════╧════════════╛"
    )
    assert queue.get().strip() == res_txt
