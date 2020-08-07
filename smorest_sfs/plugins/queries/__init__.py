"""
    sa模块
"""
from typing import Any, List, Literal, Optional, Type, Union, overload

from sqlalchemy import Table, select
from sqlalchemy.engine import RowProxy

from .abstract import _R, _S, _T
from .query import SAQuery
from .statement import SAStatement

SA_RET = Union[RowProxy, _T, _R, List[_R], List[RowProxy], None]


@overload
def execute(
    sql_cls: Type[SAStatement[_S, _T]],
    method: Literal["all"] = "all",
    *args: Any,
    **kwargs: Any
) -> List[RowProxy]:
    ...


@overload
def execute(
    sql_cls: Type[SAStatement[_S, _T]],
    method: Literal["first"],
    *args: Any,
    **kwargs: Any
) -> Optional[RowProxy]:
    ...


@overload
def execute(
    sql_cls: Type[SAStatement[_S, _T]],
    method: Literal["scalar"],
    *args: Any,
    **kwargs: Any
) -> Optional[_T]:
    ...


@overload
def execute(
    sql_cls: Type[SAQuery[_S, _R, _T]],
    method: Literal["all"] = "all",
    *args: Any,
    **kwargs: Any
) -> List[_R]:
    ...


@overload
def execute(
    sql_cls: Type[SAQuery[_S, _R, _T]],
    method: Literal["first"],
    *args: Any,
    **kwargs: Any
) -> Optional[_R]:
    ...


@overload
def execute(
    sql_cls: Type[SAQuery[_S, _R, _T]],
    method: Literal["scalar"],
    *args: Any,
    **kwargs: Any
) -> Optional[_T]:
    ...


def execute(
    sql_cls: Union[Type[SAStatement[_S, _T]], Type[SAQuery[_S, _R, _T]]],
    method: str = "all",
    *args: Any,
    **kwargs: Any
) -> SA_RET[_T, _R]:
    sql = sql_cls(*args, **kwargs)
    actions = {"all": sql.all, "first": sql.first, "scalar": sql.scalar}
    return actions[method]()


def debug_sql(
    sql_cls: Union[Type[SAStatement[_S, _T]], Type[SAQuery[_S, _R, _T]]],
    *args: Any,
    **kwargs: Any
) -> None:
    sql = sql_cls(*args, **kwargs)
    sql.debug_sql()


def render_limit_results(
    sql_cls: Union[Type[SAStatement[_S, _R]], Type[SAQuery[_S, _R, _T]]],
    *args: Any,
    **kwargs: Any
) -> None:
    sql = sql_cls(*args, **kwargs)
    sql.render_results()


def quick_render(table: Table) -> None:
    class TableRender(SAStatement[select, RowProxy]):
        def __init__(self) -> None:
            self._sa_sql = select([table])

    render = TableRender()
    render.render_results()


__all__ = [
    "quick_render",
    "debug_sql",
    "render_limit_results",
    "execute",
    "SAStatement",
    "SAQuery",
]
