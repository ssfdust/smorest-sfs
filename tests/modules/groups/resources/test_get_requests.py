#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Dict, List

import pytest

from tests._utils.launcher import AccessLauncher

if TYPE_CHECKING:
    from smorest_sfs.modules.groups.models import Group


class TestListView(AccessLauncher):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "groups")
    item_view = "Group.GroupItemView"
    listview = "Group.GroupListView"
    view = "Group.GroupView"
    login_roles = ["GroupManager"]
    groups: List["Group"]

    def test_get_options(self) -> None:
        self._get_options()

    @pytest.mark.parametrize("params, cnt", [({"name": "1"}, 1), ({"name": "test"}, 3)])
    def test_get_list(self, params: Dict[str, str], cnt: int) -> None:
        data = self._get_list(**params)
        if data:
            assert data[0].keys() > {"id", "name", "default"}
        assert len(data) == cnt

    def test_get_item(self) -> None:
        data = self._get_item(group_id=self.groups[0].id_)
        assert data.keys() >= {"id", "name"}
