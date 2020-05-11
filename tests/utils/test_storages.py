#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io

import pytest
from freezegun import freeze_time
from werkzeug.datastructures import FileStorage

from smorest_sfs.utils.storages import (
    delete_from_rel_path,
    load_avator_from_path,
    load_storage_from_path,
    save_storage_to_path,
)


@freeze_time("1994-09-11 08:20:00")
@pytest.mark.usefixtures("patch_uuid")
@pytest.mark.usefixtures("clean_dirs")
def test_read_storage_after_saved() -> None:
    store = FileStorage(
        io.BytesIO(b"abc"), "test.txt", "file", "application/octet-stream"
    )
    save_storage_to_path(store, "foo")
    assert store.read() == b"abc"


@freeze_time("1994-09-11 08:20:00")
@pytest.mark.usefixtures("patch_uuid")
@pytest.mark.usefixtures("clean_dirs")
def test_load_storage_after_saved() -> None:
    store = FileStorage(
        io.BytesIO(b"abc"), "test.txt", "file", "application/octet-stream"
    )
    pathstr = save_storage_to_path(store, "foo")
    loaded_store = load_storage_from_path("test.txt", pathstr)
    assert loaded_store.read() == b"abc"


@freeze_time("1994-09-11 08:20:00")
@pytest.mark.usefixtures("patch_uuid")
@pytest.mark.usefixtures("clean_dirs")
def test_load_storage_after_deleted() -> None:
    store = FileStorage(
        io.BytesIO(b"abc"), "test.txt", "file", "application/octet-stream"
    )
    pathstr = save_storage_to_path(store, "foo")
    delete_from_rel_path(pathstr)
    with pytest.raises(FileNotFoundError):
        load_storage_from_path("test.txt", pathstr)


@pytest.mark.parametrize(
    "avator_path", ["default/AdminAvator.jpg", "default/DefaultAvator.jpg"]
)
def test_avator_path(avator_path: str) -> None:
    storage = load_avator_from_path(avator_path)
    assert len(storage.read()) > 0
