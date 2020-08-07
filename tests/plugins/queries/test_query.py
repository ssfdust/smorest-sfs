from typing import Type, TypeVar

import pytest

from smorest_sfs.plugins.queries import (
    SAQuery,
    debug_sql,
    execute,
    render_limit_results,
)
from tests._utils.uniqueue import UniqueQueue

_R = TypeVar("_R")
_S = TypeVar("_S")
_T = TypeVar("_T")


queue: UniqueQueue[str] = UniqueQueue()


@pytest.mark.parametrize(
    "query, res_txt", ((1, ["quries", 1]), (2, ["quries", 2])), indirect=True
)
@pytest.mark.usefixtures("inject_logger")
def test_debug_sql(query: Type[SAQuery[_S, _R, _T]], res_txt: str) -> None:
    debug_sql(query)
    assert queue.get().strip() == res_txt


@pytest.mark.parametrize(
    "query, res_txt",
    ((1, ["query_tables", 1]), (2, ["query_tables", 2])),
    indirect=True,
)
@pytest.mark.usefixtures("inject_logger")
def test_render_sql(query: Type[SAQuery[_S, _R, _T]], res_txt: str) -> None:
    render_limit_results(query)
    assert queue.get().strip() == res_txt


@pytest.mark.parametrize("query", (1, 2), indirect=True)
@pytest.mark.parametrize("method", ["first", "all", "scalar"])
@pytest.mark.usefixtures("delete_items")
def test_execute_query(query: Type[SAQuery[_S, _R, _T]], method: str) -> None:
    res = execute(query, method)  # type: ignore
    assert res
