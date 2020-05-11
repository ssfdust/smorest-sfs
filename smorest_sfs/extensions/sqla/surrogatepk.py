"""
    smorest_sfs.sqla.surrogatepk
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ORM默认主键模块
"""
from typing import Any, List, Type, Union

from flask_sqlalchemy import _QueryProperty
from marshmallow import Schema
from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy_utils.types.enriched_datetime.enriched_datetime_type import (
    EnrichedDateTimeType,
)

from .db_instance import db
from .helpers import utcnow


# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK:
    """
    数据库表栏目模板

    :attr id: int 主键
    :attr deleted: bool 删除状态
    :attr modified: datetime 修改时间
    :attr created: datetime 创建时间
    """

    query: _QueryProperty

    id = Column(Integer, primary_key=True, info={"marshmallow": {"dump_only": True}})
    deleted = Column(
        Boolean,
        nullable=False,
        doc="已删除",
        default=False,
        info={"marshmallow": {"dump_only": True}},
    )
    modified = Column(
        EnrichedDateTimeType(),
        nullable=False,
        doc="修改时间",
        server_default=utcnow(),
        onupdate=db.select([utcnow()]),
        info={"marshmallow": {"format": "%Y-%m-%d %H:%M:%S", "dump_only": True}},
    )
    created = Column(
        EnrichedDateTimeType(),
        nullable=False,
        doc="创建时间",
        server_default=utcnow(),
        info={"marshmallow": {"format": "%Y-%m-%d %H:%M:%S", "dump_only": True}},
    )

    @classmethod
    def get_by_id(cls, _id: int) -> Any:
        """
        根据ID查询数据库
        """
        with db.session.no_autoflush:
            return cls.query.get_or_404(_id)

    @classmethod
    def delete_by_id(cls, _id: int, commit: bool = True) -> Any:
        """
        根据ID删除数据
        """
        item = cls.get_by_id(_id)
        return item.delete(commit)

    @classmethod
    def delete_by_ids(cls, ids: List[int], commit: bool = True) -> Union[bool, None]:
        """
        批量删除
        """
        kw = [{"id": id, "deleted": True} for id in ids]
        db.session.bulk_update_mappings(cls, kw)

        return commit and db.session.commit()

    @classmethod
    def update_by_id(
        cls,
        _id: int,
        schema: Union[Schema, Type[Schema]],
        instance: Any,
        commit: bool = True,
    ) -> Any:
        """
        根据id，Schema，以及临时实例更新元素

        :param ids: list 主键
        :param schema: Schema Schema类或实例
        :param instance: object 临时Model对象
        :param commit: bool 是否提交

        详见update_by_ma注释
        """
        item = cls.get_by_id(_id)

        item.update_by_ma(schema, instance, commit=commit)

        return item
