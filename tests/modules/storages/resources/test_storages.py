#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from typing import TYPE_CHECKING

import pytest

from tests._utils.launcher import Launcher

if TYPE_CHECKING:
    from smorest_sfs.modules.storages.models import Storages


class TestStoragesView(Launcher):

    login_roles = ["User"]
    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    def test_get(self, add_storage: "Storages") -> None:
        self.build_url("Storages.StoragesView", file_id=add_storage.id_)
        resp = self.payload()
        assert resp.data == b"abc"

    def test_put(self, add_storage: "Storages") -> None:
        self.build_url("Storages.StoragesView", file_id=add_storage.id_)
        self.payload(
            "PUT",
            data={"file": (io.BytesIO(b"789"), "new.txt")},
            content_type="multipart/form-data",
        )
        add_storage.as_stream()
        resp = self.payload()
        assert resp.data == b"789"

    def test_delete(self, add_storage: "Storages") -> None:
        self.build_url("Storages.StoragesView", file_id=add_storage.id_)
        resp = self.payload("DELETE")
        after_resp = self.payload()
        assert resp.json["code"] == 0 and after_resp.status_code == 404


class TestForceDeleteView(Launcher):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")
    login_roles = ["SuperUser"]

    def test_force_delete(self, add_storage: "Storages") -> None:
        from smorest_sfs.utils.storages import load_storage_from_path

        self.build_url("Storages.ForceDeleteView", file_id=add_storage.id_)
        self.payload("DELETE")
        path = ""
        if add_storage.path:
            path = add_storage.path[:]
        with pytest.raises(FileNotFoundError):
            load_storage_from_path("test.txt", path)


class TestUploadView(Launcher):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")
    login_roles = ["User"]

    @pytest.mark.usefixtures("clean_dirs")
    def test_post(self) -> None:
        self.build_url("Storages.UploadView", storetype="foo")
        resp = self.payload(
            "POST",
            data={"file": (io.BytesIO(b"456"), "new.txt")},
            content_type="multipart/form-data",
        )
        store_id = resp.json["data"]["file_id"]
        self.build_url("Storages.StoragesView", file_id=store_id)
        resp = self.payload()
        assert resp.data == b"456"
