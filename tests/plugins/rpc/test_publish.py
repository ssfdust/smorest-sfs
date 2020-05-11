#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable

import pytest

from smorest_sfs.plugins.rpc import Publisher, default_queues


class TestPublisher:
    @pytest.mark.parametrize("key", ["1212", {"test": 1}])
    def test_pubshlish(
        self,
        key: Any,
        listen: Callable[..., Callable[[Callable[..., None]], Callable[..., None]]],
    ) -> None:
        queue = default_queues.get_default_queue()
        p = Publisher(queue, key)
        p.publish()

        def assert_val(body: Any, message: Any) -> None:
            assert body == key
            message.ack()

        on_listen = listen(queue)(assert_val)
        on_listen()
