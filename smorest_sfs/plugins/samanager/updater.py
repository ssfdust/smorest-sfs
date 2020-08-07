"""更新类
"""
from typing import List

from marshmallow import Schema
from sqlalchemy.orm.attributes import del_attribute, get_attribute, set_attribute
from sqlalchemy_utils import naturally_equivalent

from .base import _BaseManager
from .typings import _M

BLACK_LIST = ["id", "deleted", "modified", "created"]


def _get_loadable_fileds(schema: Schema) -> List[str]:
    return [
        k for k, v in schema.fields.items() if not v.dump_only and k not in BLACK_LIST
    ]


class _Updater(_BaseManager[_M]):
    """根据marshmallow对象更新ORM对象"""

    def _assert_not_eq(self, instance: _M) -> None:
        if naturally_equivalent(self.instance(), instance):
            raise ValueError("The target Instace is the same one as the origin Instace")

    def _assert_not_in_session(self, instance: _M) -> None:
        if instance in self.session():
            raise RuntimeError("The Instance is in session")

    def _update_with(self, instance: _M, schema: Schema) -> None:
        """更新函数

        根据提供的Schema更新ORM实例，确保instance不在session中，
        否则会flush到数据中。
        而后会根据schema中非dump_only的字段更新实例，同时删除
        instance的属性。

        Args:
            instance (_M): 更新实例
            schema (Schema): 所用的schema

        Returns:
            None:

        Raises:
            ValueError: 同一实例或临时实例在session中
            RuntimeError: instance已添加到session中
        """
        self._assert_not_in_session(instance)
        self.session().add(instance)

        loadable_fields = _get_loadable_fileds(schema)
        self._setattr_from_instance(loadable_fields, instance)

        self.session().expunge(instance)
        self.session().add(self.instance())

    def _setattr_from_instance(self, fields: List[str], instance: _M) -> None:
        with self.session().no_autoflush:
            for field in fields:
                set_attribute(self.instance(), field, get_attribute(instance, field))
                del_attribute(instance, field)
