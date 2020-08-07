#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

import pytest

from tests._utils.injection import FixturesInjectBase

if TYPE_CHECKING:
    from smorest_sfs.modules.storages.models import Storages
    from werkzeug.datastructures import FileStorage


class TestStorage(FixturesInjectBase):
    fixture_names = ("flask_app", "storage", "patch_uuid", "clean_dirs", "next_store")
    storage: "Storages"
    next_store: "FileStorage"

    def test_model_save(self) -> None:
        from smorest_sfs.services.storages.handlers import StorageFactory
        from smorest_sfs.utils.storages import load_storage_from_path

        factory = StorageFactory(self.storage)
        factory.save()
        if self.storage.name and self.storage.path:
            store = load_storage_from_path(self.storage.name, self.storage.path)
        assert store.read() == b"abc" and self.storage.store.read() == b"abc"

    def test_model_load(self) -> None:
        from smorest_sfs.services.storages.handlers import StorageFactory
        from smorest_sfs.modules.storages.models import Storages

        factory = StorageFactory(self.storage)
        factory.save()
        storage = Storages.find_or_fail(self.storage.id_)
        for _ in range(3):
            storage.as_stream()
            assert storage.store.read() == b"abc"

    def test_model_update(self) -> None:
        from smorest_sfs.services.storages.handlers import StorageFactory
        from smorest_sfs.modules.storages.models import Storages

        factory = StorageFactory(self.storage)
        factory.save()
        factory.update(name="t.txt", store=self.next_store)
        storage = Storages.find_or_fail(self.storage.id_)
        storage.store = None
        assert storage.store.read() == b"efg" and storage.name == "t.txt"  # type: ignore

    def test_model_delete(self) -> None:
        from smorest_sfs.services.storages.handlers import StorageFactory
        from smorest_sfs.utils.storages import load_storage_from_path

        factory = StorageFactory(self.storage)
        factory.save()
        factory.hard_delete()
        with pytest.raises(FileNotFoundError):
            if self.storage.name and self.storage.path:
                load_storage_from_path(self.storage.name, self.storage.path)
        with pytest.raises(FileExistsError):
            self.storage.store.close()
            self.storage.as_stream()
