#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

import pytest

from smorest_sfs.modules.auth import ROLES
from tests._utils.launcher import AccessLauncher


class TestListView(AccessLauncher):

    login_roles = [ROLES.EmailTemplateManager]
    fixture_names = ("flask_app_client", "flask_app", "regular_user", "email_templates")
    listview = "EmailTemplate.EmailTemplateListView"
    view = "EmailTemplate.EmailTemplateView"
    item_view = "EmailTemplate.EmailTemplateItemView"

    def test_get_options(self) -> None:
        self._get_options()

    @pytest.mark.parametrize("params, cnt", [({"name": "de"}, 1)])
    def test_get_list(self, params: Dict[str, str], cnt: int) -> None:
        data = self._get_list(**params)
        if data:
            assert data[0].keys() > {"id", "name", "template"}
        assert len(data) == cnt

    def test_get_item(self) -> None:
        data = self._get_item(email_template_id=1)
        assert data.keys() >= {"id", "name", "deleted", "template"}
