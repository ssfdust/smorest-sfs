#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator
import pytest

from smorest_sfs.modules.email_templates.models import EmailTemplate


@pytest.mark.usefixtures("flask_app")
def test_email_template(temp_db_instance_helper: Callable[..., Iterator[Any]]) -> None:
    for email_template in temp_db_instance_helper(EmailTemplate(name="test", template="")):
        assert str(email_template) == "test"
