#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

import pytest

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.projects.models import Project
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "project_items")
    item_view = "Project.ProjectItemView"
    listview = "Project.ProjectListView"
    view = "Project.ProjectView"
    login_roles = [ROLES.ProjectManager]
    project_items: List[Project]

    def test_get_options(self) -> None:
        self._get_options()

    @pytest.mark.parametrize("params, cnt", [({"name": "1"}, 1), ({"name": "name"}, 3)])
    def test_get_list(self, params: Dict[str, str], cnt: int) -> None:
        data = self._get_list(**params)
        if data:
            assert data[0].keys() > {"id", "name"}
        assert len(data) == cnt

    def test_get_item(self) -> None:
        data = self._get_item(project_id=self.project_items[0].id)
        assert data.keys() >= {"id", "name"}
