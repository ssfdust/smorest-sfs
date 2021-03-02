#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, List, Dict

import pytest

from smorest_sfs.modules.auth import ROLES
from tests._utils.launcher import AccessLauncher

if TYPE_CHECKING:
    from smorest_sfs.modules.projects.models import Project


class TestListView(AccessLauncher):

    login_roles = [ROLES.ProjectManager]
    fixture_names = ("flask_app_client", "flask_app", "regular_user", "projects")
    item_view = "Project.ProjectItemView"
    listview = "Project.ProjectListView"
    view = "Project.ProjectView"

    def test_get_options(self) -> None:
        self._get_options()

    @pytest.mark.parametrize("params, cnt", [({"name": "1"}, 1), ({"name": "name"}, 3)])
    def test_get_list(self, params: Dict[str, str], cnt: int) -> None:
        data = self._get_list(**params)
        if data:
            assert data[0].keys() > {"id", "name"}
        assert len(data) == cnt

    def test_get_item(self) -> None:
        data = self._get_item(project_id=self.projects[0].id_)
        assert data.keys() >= {"id", "name"}
