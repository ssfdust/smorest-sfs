"""
    smorest_sfs.extensions.errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    自定义错误类型
"""
from psycopg2.errors import StringDataRightTruncation, UniqueViolation
from sqlalchemy.exc import DBAPIError

from .db_instance import db


class DuplicateEntry(Exception):
    """重复的类型"""


class CharsTooLong(Exception):
    """字符过长"""


err_mapping = {
    UniqueViolation: DuplicateEntry,
    StringDataRightTruncation: CharsTooLong,
}


def pgerr_to_customerr(err: DBAPIError) -> None:  # type: ignore
    """转换PG的错误为自定义类型的错误并回滚"""
    for err_cls, custom_err_cls in err_mapping.items():
        if isinstance(err.orig, err_cls):
            db.session.rollback()
            raise custom_err_cls(str(err))
