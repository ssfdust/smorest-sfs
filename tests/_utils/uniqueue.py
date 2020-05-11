#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import queue
from typing import TYPE_CHECKING, TypeVar

T = TypeVar("T")

if TYPE_CHECKING:
    SimpleQueue = queue.SimpleQueue
else:

    class FakeGenericMeta(type):
        def __getitem__(self, item):
            return self

    class SimpleQueue(queue.SimpleQueue, metaclass=FakeGenericMeta):
        pass


class UniqueQueue(SimpleQueue[T]):

    _queue: UniqueQueue[T]

    def __new__(cls) -> UniqueQueue[T]:
        if not hasattr(cls, "_queue"):
            orig = super(UniqueQueue, cls)
            cls._queue = orig.__new__(cls)

        return cls._queue
