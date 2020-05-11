#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Dict, TypeVar

from flask import jsonify
from loguru import logger

from smorest_sfs.extensions import jwt_instance as jwt
from smorest_sfs.modules.users.models import User

from .helpers import is_token_revoked

Response = TypeVar("Response")


@jwt.unauthorized_loader
def unauthorized_callback(_: Any) -> Any:
    logger.error("未受权的访问")
    response = jsonify({"code": 401, "msg": "未授权的访问"})
    response.status_code = 401
    return response


@jwt.expired_token_loader
def token_expired() -> Any:
    response = jsonify({"code": 402, "msg": "登录已过期"})
    logger.warning("登录过期")
    response.status_code = 402
    return response


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token: Dict[str, str]) -> bool:
    return is_token_revoked(decrypted_token)


@jwt.user_loader_callback_loader
def get_user(identity: str) -> User:
    return User.get_by_keyword(identity)
