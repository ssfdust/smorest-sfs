"""
    smorest_sfs.extensions.api.decorators
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    分页装饰器模块
"""

import functools
from typing import Any, Callable, Dict, List, Union

import marshmallow as ma
from flask import request, url_for
from flask_sqlalchemy import Pagination

from smorest_sfs.extensions.sqla import Model


class PaginationParametersSchema(ma.Schema):
    """分页Query参数

    :attr page 页码
    :attr per_page 分页数目
    """

    class Meta:
        # pylint: disable=C0115
        ordered = True

    page = ma.fields.Integer(missing=1, validate=ma.validate.Range(min=1), doc="页码")
    per_page = ma.fields.Integer(
        missing=10, validate=ma.validate.Range(min=1, max=100), doc="分页数目"
    )


def generate_links(p: Pagination, per_page: int, **kwargs: Any) -> Dict[str, Any]:
    """生成分页相关信息

    next: 下一页
    prev: 前一页
    first: 首页
    last: 尾页
    """
    links = {}
    if p.has_next:
        links["next"] = url_for(
            request.endpoint, page=p.next_num, per_page=per_page, **kwargs
        )
    if p.has_prev:
        links["prev"] = url_for(
            request.endpoint, page=p.prev_num, per_page=per_page, **kwargs
        )
    links["first"] = url_for(request.endpoint, page=1, per_page=per_page, **kwargs)
    links["last"] = url_for(request.endpoint, page=p.pages, per_page=per_page, **kwargs)

    return links


def paginate(max_per_page: int = 10) -> Callable[..., Any]:
    """
    分页装饰器

    :param max_per_page 最大分页数目

    将返回的BaseQuery类型转化为分页，返回形如：
    {
        "code": 0,
        "data": [items...],
        "meta": {
            "page": 10,
            "per_page": 10,
            "total": 1000,
            "pages": 100
            "links": {
                "next": url,
                "prev": url,
                "first": url,
                "last": url
            }
        }
    }
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # pylint: disable=W0212
        parameters = {
            "in": "query",
            "schema": PaginationParametersSchema,
        }

        # 注入apidoc显示注释等内容
        _apidoc = getattr(func, "_apidoc", {})
        _apidoc.setdefault("parameters", []).append(parameters)
        setattr(func, "_apidoc", _apidoc)

        @functools.wraps(func)
        def wrapped(
            *args: Any, **kwargs: Any
        ) -> Dict[str, Union[Dict[str, int], str, int, List[Model]]]:
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", max_per_page, type=int)
            query = func(*args, **kwargs)
            p = query.paginate(page, per_page)

            meta = {
                "page": page,
                "per_page": per_page,
                "total": p.total,
                "pages": p.pages,
            }

            meta["links"] = generate_links(p, per_page, **kwargs)
            result = {"data": p.items, "meta": meta, "code": 0}

            return result

        return wrapped

    return decorator
