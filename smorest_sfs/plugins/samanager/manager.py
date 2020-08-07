"""Schema与ORM关联模块

此模块提供SqlaManager类用以映射

此方法用以更新Sqla实例的字段，基于一个marshmallow类或实例，
根据marshmallow类的load字段加载。由于需要一个临时变量的
instance，对于需要同时处理复杂relationship的子关系需要增
加指定active_history=True来跟踪变化以维持正确的加载。

示例：
>>> from marshmallow import Schema, fields
>>> class RemoteSchema(Schema):
        id_ = fields.Int(data_key="id")
        name = fields.Str()
>>> class LocalSchema(Schema):
        id_ = fields.Int(data_key="id")
        name = fields.Str()
        remote = fields.Nested(RemoteSchema)
>>> class Remote(Model):
        id_ = Column("id", Integer(), primary_key=True)
        name = Column(String(80))
>>> class Local(Model):
        id = Column(Integer(), primary_key=True)
        remote_id = Column(Integer())
        remote = relationship(
            "Remote",
            active_history=True,
            backref=backref('local', active_history=True)
        )
>>> manager = SqlaManager(session)
>>> manager.register_mappings(Local, LocalSchema)
>>> manager.register_mappings(Remote, Schema)
>>> local = Local(remote=Remote(name="remote"))
>>> session.add(local)
>>> session.commit()
>>> temp = Local(remote=Remote(name="remote1"))
>>> manager.inst_with(local)  # manager.pk_with(Local, local.id)
>>> manager.update_with(temp)

在这里需要修改Remote中name以及关系时。
"""
from typing import Type

from sqlalchemy.orm import Session

from .mapping import _MappingManager
from .typings import _M, OPT_SCHEMA
from .updater import _Updater


class _SqlaManager(_Updater[_M], _MappingManager[_M]):
    def update_with(
        self, instance: _M, schema: OPT_SCHEMA = None, commit: bool = True,
    ) -> _M:
        """更新当前实例

        用instance（临时）来更新SqlaManager中注入的instance，
        当Schema不为空的时候，将会根据提供的Schema的可写字段
        进行更新，否则将会去去寻找已注册的映射字段进行更新。

        Args:
            instance (_M): 用以更新的实例
            schema (OPT_SCHEMA): Schema或None
            commit (bool): 是否提交session

        Raises:
            ValueError: 临时实例和注入实例不允许一样
            RuntimeError: 临时实例在session中
            KeyError: 未找到ORM对应的Schema
        """
        self._assert_not_eq(instance)
        schema = self._get_schema(schema)

        self._update_with(instance, schema)

        return self.instance()


class SqlaManager(_SqlaManager[_M]):
    """序列化ORM更新管理器

    此类负责序列化与数据更新，通过设置mapping来更新对应关系，
    而后通过临时实例来更新数据内容。

    Attribute:
        instance (_M): 需要更新的实例
        session (Session): 当前session
    """

    def __init__(self, session: Session):
        """初始化函数，注入session"""
        self._instance: _M
        self._session = session

    def inst_with(self, instance: _M) -> None:
        """初始化实例

        Args:
            instance (_M): 待更新的实例

        Returns:
            None:
        """
        self._instance = instance

    def pk_with(self, inst_cls: Type[_M], id_: int) -> None:
        """使用Model以及key初始化实例"""
        with self._session.no_autoflush:
            self._instance = self._session.query(inst_cls).get(id_)  # type: ignore

    def instance(self) -> _M:
        """返回当前操作实例"""
        return self._instance

    def session(self) -> Session:
        """返回当前session"""
        return self._session
