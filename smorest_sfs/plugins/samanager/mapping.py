"""映射关系管理

此模块提供一个映射关系管理类_MappingManager，
用以管理ORM与Schema的对应管理关系，

* _MappingManager.get_mappings获取当前对应关系。

* _MappingManager.register_mappings注册新关联。
"""

from marshmallow import Schema

from .base import _BaseManager
from .typings import _M, MAPPING_TYPE, OPT_SCHEMA, STRC
from .utils import get_the_obj as _get_the_obj


class _MappingManager(_BaseManager[_M]):
    """管理映射对象关系

    此类用以管理ORM与Schema对应关系，对应关系存储在
    _registed_sa_mapping这个类属性下。该属性与类绑定，
    且唯一。
    """

    _registed_sa_mapping: MAPPING_TYPE[_M] = {}

    @classmethod
    def register_mappings(cls, sa_model: STRC[_M], ma_schema: STRC[Schema]) -> None:
        """注册ORM与Schema关联关系

        可以传两个对象或者字符串，如果是传递的字符串，会将字符串解析成模块
        中的对象。

        Args:
            sa_model (STRC[_M]): ORM或者ORM对应的模块字符串
            ma_schema (STRC[Schema]): Schema或者Schema对应的字符串

        Returns:
            None:
        """
        sa_model = _get_the_obj(sa_model)
        ma_schema = _get_the_obj(ma_schema)
        cls._registed_sa_mapping[sa_model] = ma_schema

    @classmethod
    def get_mappings(cls) -> MAPPING_TYPE[_M]:
        """获取当前对应关系"""
        return cls._registed_sa_mapping

    def _get_schema(self, schema: OPT_SCHEMA) -> Schema:
        _schema: Schema
        if not schema and self.instance:
            _schema = self._registed_sa_mapping[type(self.instance())]()
        elif isinstance(schema, Schema):
            _schema = schema
        elif schema is not None and issubclass(schema, Schema):
            _schema = schema()
        return _schema
