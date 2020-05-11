#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io

import pytest
from werkzeug.datastructures import FileStorage

from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.services.storages.handlers import StorageFactory


@pytest.fixture
def store() -> FileStorage:
    return FileStorage(io.BytesIO(b"abc"), "test.txt", "file", "text/txt")


@pytest.fixture
def storage(store: FileStorage) -> Storages:
    # pylint: disable=W0621
    return Storages(name="test.txt", storetype="foo", store=store)


@pytest.fixture
def next_store() -> FileStorage:
    return FileStorage(io.BytesIO(b"efg"), "test.txt", "file", "text/txt")


@pytest.fixture
def add_storage(store: FileStorage) -> Storages:
    # pylint: disable=W0621
    factory = StorageFactory(Storages(name="test.txt", storetype="foo", store=store))
    storage: Storages = factory.save()
    return storage
