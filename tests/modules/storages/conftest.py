#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from typing import TYPE_CHECKING

import pytest
from werkzeug.datastructures import FileStorage

if TYPE_CHECKING:
    from smorest_sfs.modules.storages.models import Storages


@pytest.fixture
def store() -> FileStorage:
    return FileStorage(io.BytesIO(b"abc"), "test.txt", "file", "text/txt")


@pytest.fixture
def storage(store: FileStorage) -> "Storages":
    # pylint: disable=W0621
    from smorest_sfs.modules.storages.models import Storages

    return Storages(name="test.txt", storetype="foo", store=store)  # type: ignore


@pytest.fixture
def next_store() -> FileStorage:
    return FileStorage(io.BytesIO(b"efg"), "test.txt", "file", "text/txt")


@pytest.fixture
def add_storage(store: FileStorage) -> "Storages":
    # pylint: disable=W0621
    from smorest_sfs.services.storages.handlers import StorageFactory
    from smorest_sfs.modules.storages.models import Storages

    factory = StorageFactory(Storages(name="test.txt", storetype="foo", store=store))  # type: ignore
    storage: "Storages" = factory.save()
    return storage
