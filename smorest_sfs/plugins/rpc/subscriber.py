#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Iterator

from amqp.exceptions import NotFound
from kombu.pools import connections

from .base import RPCBase


class Subscriber(RPCBase):
    def subscribe(self, no_ack: bool = False, requeue: bool = False) -> Iterator[Any]:
        """
        重载数值
        """
        if self.conn:
            for i in self._subscribe(no_ack, requeue):
                yield i
        else:
            raise RuntimeError("No Connection Found")

    def _subscribe(self, no_ack: bool = False, requeue: bool = False) -> Iterator[Any]:
        """
        重载数值
        """
        for i in self.extract_from_queue(no_ack):
            yield i.payload
            if no_ack is False and requeue is False:
                i.ack()
            elif requeue is True:
                i.requeue()

    def extract_from_queue(self, no_ack: bool = False) -> Iterator[Any]:
        """
        从队列加载并返回列表
        :param no_ack 是否ack
        """
        pool = connections[self.conn]

        with pool.acquire_channel(block=True) as (_, channel):
            binding = self.queue(channel)

            for _ in range(self.limit):
                try:
                    msg = binding.get(accept=["json"], no_ack=no_ack)
                    if not msg:
                        break
                    yield msg
                except NotFound:
                    break
