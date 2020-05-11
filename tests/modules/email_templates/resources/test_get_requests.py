#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    login_roles = [ROLES.EmailTemplateManager]
    fixture_names = ("flask_app_client", "flask_app", "regular_user")
    listview = "EmailTemplate.EmailTemplateListView"
    view = "EmailTemplate.EmailTemplateView"
    item_view = "EmailTemplate.EmailTemplateItemView"

    def test_get_options(self) -> None:
        self._get_options()

    def test_get_list(self) -> None:
        data = self._get_list(name="t")
        assert data[0].keys() > {"id", "name", "template"}

    def test_get_item(self) -> None:
        data = self._get_item(email_template_id=1)
        assert data.keys() >= {"id", "name", "deleted", "template"}
