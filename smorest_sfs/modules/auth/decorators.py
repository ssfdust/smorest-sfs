#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    系统的权限装饰器模块

    为请求添加权限装饰器，参数为权限
"""
from copy import deepcopy
from functools import wraps
from typing import Any, Callable

from flask_jwt_extended import current_user, jwt_refresh_token_required, jwt_required
from flask_smorest import abort  # type: ignore
from loguru import logger

# 源码来自
# https://github.com/Nobatek/flask-rest-api/issues/36#issuecomment-460826257


def __set_apidoc(
    wrapper: Callable[..., Any],
    func: Callable[..., Any],
    security_mehod: str = "api_key",
) -> Callable[..., Any]:
    _apidoc = deepcopy(getattr(func, "_apidoc", {}))
    _apidoc["manual_doc"] = {"security": [{security_mehod: []}]}
    setattr(wrapper, "_apidoc", _apidoc)
    return wrapper


def doc_login_required(func: Callable[..., Callable[..., Any]]) -> Callable[..., Any]:
    """
    登录限制装饰器

    为API添加登录限制，同时添加OpenAPI注释，使用装饰器后
    只有带有合法jwt token的请求才能访问。

    用法：
    >>> class SampleView(MethodView):
            @doc_login_required
            def get(self):
                return {'code': 0}
    """
    # pylint: disable=W0212
    # 获取登录函数
    auth_required_func = jwt_required(func)

    # 封装函数
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return auth_required_func(*args, **kwargs)

    # 增加验证
    wrapper = __set_apidoc(wrapper, func)  # type: ignore

    return wrapper


def doc_refresh_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    刷新Token限制装饰器

    Refresh Token:
    在Jwt架构中，除了登录用的token，还有刷新token用的token。

    为API添加刷新限制，同时添加OpenAPI注释，使用装饰器后
    只有带有合法refresh token的请求才能访问。

    用法：
    >>> class SampleView(MethodView):
            @doc_refresh_required
            def get(self):
                return {'code': 0}
    """
    # pylint: disable=W0212
    # 获取刷新函数
    refresh_required_func = jwt_refresh_token_required(func)

    # 封装刷新函数
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return refresh_required_func(*args, **kwargs)

    # 增加swagger信息
    wrapper = __set_apidoc(wrapper, func, "refresh_key")  # type: ignore

    return wrapper


def permission_required(*permissions: str) -> Callable[..., Any]:
    """
    权限验证

    :param permissions: tuple 权限列

    为API添加权限限制，同时添加OpenAPI注释，使用装饰器后
    只有带有才能访问。必须在doc_login_required装饰器后。

    用法：
    >>> class SampleView(MethodView):
            @doc_login_required
            @permission_required('Permission')
            def get(self):
                return {'code': 0}
    """

    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            if not all(
                permission in [p.name for p in current_user.permissions]
                for permission in permissions
            ):
                logger.error(f"{current_user.email}不具备{permissions}")
                abort(403, message="禁止访问")
            return func(*args, **kwargs)

        return inner

    return wrapper


def role_required(*roles: str) -> Callable[..., Any]:
    """
    角色验证

    :param roles: tuple 角色列

    为API添加角色限制，同时添加OpenAPI注释，使用装饰器后
    只有带有才能访问。必须在doc_login_required装饰器后。

    用法：
    >>> class SampleView(MethodView):
            @doc_login_required
            @role_required('Role')
            def get(self):
                return {'code': 0}
    """

    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            if not all(role in [p.name for p in current_user.roles] for role in roles):
                logger.error(f"{current_user.email}不具备{roles}")
                abort(403, message="禁止访问")
            return func(*args, **kwargs)

        return inner

    return wrapper
