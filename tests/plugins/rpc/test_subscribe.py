#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any

import pytest

from smorest_sfs.plugins.rpc import Publisher, Subscriber, default_queues


class TestSubscriber:
    publisher: Publisher
    subscriber: Subscriber
    key: Any

    @pytest.fixture(autouse=True)
    def setup_pubsub(self) -> None:
        queue = default_queues.get_default_queue()

        setattr(self, "publisher", Publisher(queue))
        setattr(self, "subscriber", Subscriber(queue))

    def publish(self, key: Any) -> None:
        self.publisher.value = key
        self.publisher.publish()

    @pytest.mark.usefixtures("flask_app")
    @pytest.mark.parametrize("key", ["1212", {"test": 1}])
    def test_subscribe(self, key: Any) -> None:
        self.publish(key)
        for res in self.subscriber.subscribe():
            assert res == key

    @pytest.mark.usefixtures("flask_app")
    @pytest.mark.parametrize("key", ["1212", {"test": 1}])
    def test_subscribe_noack(self, key: Any) -> None:
        self.publish(key)
        for res in self.subscriber.subscribe(no_ack=True):
            assert res == key

    @pytest.mark.usefixtures("flask_app")
    @pytest.mark.parametrize("key", ["1212", {"test": 1}])
    def test_subscribe_requeue(self, key: Any) -> None:
        self.publish(key)
        for _ in range(10):
            RUN = False
            for res in self.subscriber.subscribe(requeue=True):
                RUN = True
                assert res == key
            assert RUN

        list(self.subscriber.subscribe())
