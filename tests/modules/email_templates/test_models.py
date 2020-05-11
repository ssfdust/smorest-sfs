#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.extensions.flask import Flask
from smorest_sfs.modules.email_templates.models import EmailTemplate


def test_get_template(flask_app: Flask) -> None:
    name = str(EmailTemplate.create(name="test", template="111"))
    assert name == "test" and EmailTemplate.get_template(name) == "111"
