# Copyright 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    app.services.auth.confirm
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    验证模块
"""
from datetime import timedelta
from typing import Optional

from flask import current_app as app
from flask_jwt_extended import create_access_token, get_raw_jwt
from flask_smorest import abort
from sqlalchemy.orm.exc import NoResultFound

from smorest_sfs.modules.auth.helpers import add_token_to_database
from smorest_sfs.modules.auth.models import TokenBlackList
from smorest_sfs.modules.users.models import User


def confirm_current_token(token_type: str, revoked: bool = True) -> User:
    """
    验证token

    :param jti: str jti字符串
    :param token_type: str token类型
    :param revoked 是否撤销token
    :return (state, user)
    """
    try:
        jti = get_raw_jwt()["jti"]
        token = TokenBlackList.where(jti=jti, token_type=token_type).one()
        token.update(revoked=revoked)
        user = User.get_by_keyword(token.user_identity)
    except NoResultFound:
        abort(403, message="token无效")
    return user


def generate_confirm_token(user: User, token_type: str) -> str:
    token: str = create_access_token(
        identity=user.email, expires_delta=timedelta(days=1)
    )
    add_token_to_database(token, app.config["JWT_IDENTITY_CLAIM"], token_type)

    return token
