"""
    smorest_sfs.modules.auth.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    auth辅助文件
"""
from datetime import datetime
from typing import Dict, Optional

from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import NoResultFound

from .models import TokenBlackList


def _epoch_utc_to_datetime(epoch_utc: str) -> datetime:
    """
    转换时间戳为日期时间
    """
    return datetime.fromtimestamp(float(epoch_utc))


def is_token_revoked(decoded_token: Dict[str, str]) -> bool:
    """
    从数据库中寻找token是否被撤销
    """
    jti: str = decoded_token["jti"]
    try:
        token: TokenBlackList = TokenBlackList.where(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def add_token_to_database(
    encoded_token: str,
    identity_claim: str,
    custom_token_type: Optional[str] = None,
    allow_expired: bool = False,
) -> None:
    """
    将新的Token解码后加入到数据库

    :param custom_token_type: 自定义的token类型
    :param identity_claim: 指定的认证字段
    """
    decoded_token = decode_token(encoded_token, allow_expired=allow_expired)
    jti = decoded_token["jti"]
    token_type = decoded_token["type"] if not custom_token_type else custom_token_type
    user_identity = decoded_token[identity_claim]
    expires = _epoch_utc_to_datetime(decoded_token["exp"])
    revoked = False
    TokenBlackList.create(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )
