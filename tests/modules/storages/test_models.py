#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.services.storages.handlers import StorageFactory
from smorest_sfs.utils.storages import FileStorage, load_storage_from_path
from tests._utils.injection import FixturesInjectBase


class TestStorage(FixturesInjectBase):
    fixture_names = ("flask_app", "storage", "patch_uuid", "clean_dirs", "next_store")
    storage: Storages
    next_store: FileStorage

    def test_model_save(self) -> None:
        factory = StorageFactory(self.storage)
        factory.save()
        store = load_storage_from_path(self.storage.name, self.storage.path)
        assert store.read() == b"abc" and self.storage.store.read() == b"abc"  # type: ignore

    def test_model_load(self) -> None:
        factory = StorageFactory(self.storage)
        factory.save()
        storage = Storages.get_by_id(self.storage.id)
        for _ in range(3):
            storage.as_stream()
            assert storage.store.read() == b"abc"

    def test_model_update(self) -> None:
        factory = StorageFactory(self.storage)
        factory.save()
        factory.update(name="t.txt", store=self.next_store)
        storage = Storages.get_by_id(self.storage.id)
        storage.store = None
        assert storage.store.read() == b"efg" and storage.name == "t.txt"  # type: ignore

    def test_model_delete(self) -> None:
        factory = StorageFactory(self.storage)
        factory.save()
        factory.hard_delete()
        with pytest.raises(FileNotFoundError):
            load_storage_from_path(self.storage.name, self.storage.path)
        with pytest.raises(FileExistsError):
            self.storage.store.close()
            self.storage.as_stream()
