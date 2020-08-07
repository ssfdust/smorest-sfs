"""定义SqlaManager的基类

模拟Rust的triat，将数据与方法分离
"""
from abc import ABC, abstractmethod
from typing import Generic

from sqlalchemy.orm import Session

from .typings import _M


class _BaseManager(ABC, Generic[_M]):
    """Manager的trait

    必须实现instance与session方法，以获取
    当前处理的对象以及session
    """

    @abstractmethod
    def instance(self) -> _M:
        ...  # pragma: no cover

    @abstractmethod
    def session(self) -> Session:
        ...  # pragma: no cover
