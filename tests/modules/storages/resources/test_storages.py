#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

import pytest
from flask import url_for

from smorest_sfs.modules.auth.permissions import ROLES
from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.modules.users.models import User
from smorest_sfs.utils.storages import load_storage_from_path
from tests._utils.injection import FixturesInjectBase


class TestStoragesView(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app")

    def test_get(self, regular_user: User, add_storage: Storages) -> None:
        with self.flask_app_client.login(regular_user, [ROLES.User]) as client:
            resp = client.get(f"/api/v1/storages/{add_storage.id}")
            assert resp.data == b"abc"

    def test_put(self, regular_user: User, add_storage: Storages) -> None:
        with self.flask_app_client.login(regular_user, [ROLES.User]) as client:
            store_id = add_storage.id
            client.put(
                f"/api/v1/storages/{store_id}",
                data={"file": (io.BytesIO(b"789"), "new.txt")},
                content_type="multipart/form-data",
            )
            add_storage.as_stream()
            resp = client.get(f"/api/v1/storages/{add_storage.id}")
            assert resp.data == b"789"

    def test_delete(self, regular_user: User, add_storage: Storages) -> None:
        with self.flask_app_client.login(regular_user, [ROLES.User]) as client:
            resp = client.delete(f"/api/v1/storages/{add_storage.id}")
            after_resp = client.get(f"/api/v1/storages/{add_storage.id}")
            assert resp.json["code"] == 0 and after_resp.status_code == 404


class TestForceDeleteView(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app")

    def test_force_delete(self, regular_user: User, add_storage: Storages) -> None:
        file_id = add_storage.id
        path = add_storage.path[:]
        with self.flask_app_client.login(regular_user, [ROLES.SuperUser]) as client:
            with self.flask_app.test_request_context():
                client.delete(url_for("Storages.ForceDeleteView", file_id=file_id))
                with pytest.raises(FileNotFoundError):
                    load_storage_from_path("test.txt", path)


class TestUploadView(FixturesInjectBase):
    fixture_names = ("flask_app_client", "flask_app")

    @pytest.mark.usefixtures("clean_dirs")
    def test_post(self, regular_user: User) -> None:
        with self.flask_app_client.login(regular_user, [ROLES.User]) as client:
            with self.flask_app.test_request_context():
                resp = client.post(
                    url_for("Storages.UploadView", storetype="foo"),
                    data={"file": (io.BytesIO(b"456"), "new.txt")},
                    content_type="multipart/form-data",
                )
                store_id = resp.json["data"]["file_id"]
                resp = client.get(url_for("Storages.StoragesView", file_id=store_id))
                assert resp.data == b"456"
