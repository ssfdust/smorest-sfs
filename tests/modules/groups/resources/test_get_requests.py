#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Dict
import pytest

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.groups.models import Group
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "group_items")
    item_view = "Group.GroupItemView"
    listview = "Group.GroupListView"
    view = "Group.GroupView"
    login_roles = [ROLES.GroupManager]
    group_items: List[Group]

    def test_get_options(self) -> None:
        self._get_options()

    @pytest.mark.parametrize("params, cnt", [({"name": "1"}, 1), ({"name": "test"}, 3)])
    def test_get_list(self, params: Dict[str, str], cnt: int) -> None:
        data = self._get_list(**params)
        if data:
            assert data[0].keys() > {"id", "name", "default"}
        assert len(data) == cnt

    def test_get_item(self) -> None:
        data = self._get_item(group_id=self.group_items[0].id)
        assert data.keys() >= {"id", "name"}
