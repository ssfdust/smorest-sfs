#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.projects.models import Project


@pytest.mark.usefixtures("flask_app")
def test_project() -> None:
    name = str(Project.create(name="test"))
    assert name == "test"