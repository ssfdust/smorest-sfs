from typing import TYPE_CHECKING, Any, Tuple

import pytest

from .uniqueue import UniqueQueue

if TYPE_CHECKING:
    from loguru import Message
    from loguru import Logger


def log_to_queue(record: "Message") -> None:
    queue: UniqueQueue[str] = UniqueQueue()
    queue.put(record.record["message"])


def inject_logger(logger: "Logger") -> int:
    return logger.add(log_to_queue, serialize=False)


def uninject_logger(logger: "Logger", logger_id: int) -> None:
    logger.remove(logger_id)


class FixturesInjectBase:

    fixture_names: Tuple[str, ...] = tuple()

    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request: Any) -> None:
        names = self.fixture_names
        for name in names:
            setattr(self, name, request.getfixturevalue(name))
