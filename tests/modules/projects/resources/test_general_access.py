#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any

import pytest
from flask import url_for

from tests._utils.launcher import Launcher


class TestGeneralAccess(Launcher):
    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    @pytest.mark.parametrize(
        "http_method, view, kw",
        (
            ("GET", "Project.ProjectListView", {}),
            ("GET", "Project.ProjectView", {}),
            ("POST", "Project.ProjectView", {}),
            ("DELETE", "Project.ProjectView", {}),
            ("GET", "Project.ProjectItemView", {"project_id": 1}),
            ("PUT", "Project.ProjectItemView", {"project_id": 1}),
            ("DELETE", "Project.ProjectItemView", {"project_id": 1}),
        ),
    )
    def test_unauthorized_access(self, http_method: str, view: str, kw: Any) -> None:
        with self.flask_app.test_request_context():
            url = url_for(view, **kw)
            response = self.flask_app_client.open(method=http_method, path=url)
            assert response.status_code == 401

    @pytest.mark.parametrize(
        "http_method, view, kw",
        (
            ("GET", "Project.ProjectListView", {}),
            ("GET", "Project.ProjectView", {}),
            ("POST", "Project.ProjectView", {}),
            ("DELETE", "Project.ProjectView", {}),
            ("GET", "Project.ProjectItemView", {"project_id": 1}),
            ("PUT", "Project.ProjectItemView", {"project_id": 1}),
            ("DELETE", "Project.ProjectItemView", {"project_id": 1}),
        ),
    )
    def test_forbbden_access(self, http_method: str, view: str, kw: Any) -> None:
        with self.flask_app.test_request_context():
            with self.flask_app_client.login(self.regular_user, []) as client:
                url = url_for(view, **kw)
                response = client.open(method=http_method, path=url)
                assert response.status_code == 403
