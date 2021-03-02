#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

import pytest

from tests._utils.launcher import ModifyLauncher


class TestProjectModify(ModifyLauncher):
    items = "projects"
    fixture_names = ("flask_app_client", "flask_app", "regular_user", "db",) + (items,)
    view = "Project.ProjectView"
    item_view = "Project.ProjectItemView"
    login_roles = ["ProjectManager"]
    edit_param_key = "project_id"

    def test_add(self, project_args: Dict[str, str]) -> None:
        data = self._add_request(project_args)
        assert data.keys() > {"id", "name"}

    def test_delete(self) -> None:
        self._delete_request()

    def test_item_modify(self) -> None:
        data = self._item_modify_request(json={"name": "renamed"})
        assert data["name"] == "renamed"

    def test_item_delete(self) -> None:
        self._item_delete_request()
