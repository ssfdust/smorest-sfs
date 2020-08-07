"""
    smorest_sfs.sqla.surrogatepk
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ORM默认主键模块
"""
from sqlalchemy import Boolean, Column, Integer, select
from sqlalchemy_utils.types.enriched_datetime.enriched_datetime_type import (
    EnrichedDateTimeType,
)

from .helpers import utcnow

now = utcnow()
update_now = select([now])


class SurrogatePK:
    """默认主键"""

    id_ = Column("id", Integer, primary_key=True)
    deleted = Column(Boolean, doc="已删除", default=False,)
    modified = Column(
        EnrichedDateTimeType(),
        doc="修改时间",
        server_default=now,
        onupdate=update_now,
        nullable=False,
    )
    created = Column(
        EnrichedDateTimeType(), doc="创建时间", server_default=utcnow(), nullable=False
    )
