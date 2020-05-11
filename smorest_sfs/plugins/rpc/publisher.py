# Copyright 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    smorest_sfs.plugin.rpc
    ~~~~~~~~~~~~~~~~~~~~~~~~

    rabbitMQ存储模块
"""
from typing import Any, Optional

from kombu.pools import producers

from .base import RPCBase


class Publisher(RPCBase):
    """
    存储器

    :param value: 值
    :param exchange: 交换机名
    :param expires: 过期时长
    :param limit: 最大限制
    :parma routing_key: 路由名
    :param auto_delete: 是否自动删除
    """

    def _publish(
        self, value: Optional[Any] = None, expiration: Optional[int] = None
    ) -> None:
        """ 保存

        :param expiration 过期时间
        """
        with producers[self.conn].acquire(block=True) as producer:
            producer.publish(
                value if value else self.value,
                exchange=self.queue.exchange,
                routing_key=self.queue.routing_key,
                correlation_id=self.queue.routing_key,
                serializer="json",
                retry=True,
                declare=[self.queue],
                delivery_mode=2,
                expiration=expiration,
            )

    def publish(
        self, value: Optional[Any] = None, expiration: Optional[int] = None
    ) -> None:
        if self.conn:
            self._publish(value, expiration)
