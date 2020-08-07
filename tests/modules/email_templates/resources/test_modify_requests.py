#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

from tests._utils.launcher import ModifyLauncher


class TestEmailTemplateModify(ModifyLauncher):

    items = "email_templates"
    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "email_templates",
        "db",
    )
    login_roles = ["EmailTemplateManager"]
    item_view = "EmailTemplate.EmailTemplateItemView"
    view = "EmailTemplate.EmailTemplateView"
    edit_param_key = "email_template_id"

    def test_add(self, email_template_args: Dict[str, str]) -> None:
        from smorest_sfs.modules.email_templates.models import EmailTemplate

        data = self._add_request(email_template_args)
        assert data.keys() >= {"id", "name", "template"}

        EmailTemplate.where(id_=data["id"]).delete()
        self.db.session.commit()

    def test_delete(self) -> None:
        self._delete_request()

    def test_item_modify(self) -> None:
        json = {"name": "renamed", "template": "renamed"}
        data = self._item_modify_request(json)
        assert data["name"] == "renamed" and data["template"] == "renamed"

    def test_item_delete(self) -> None:
        self._item_delete_request()
