#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator

import pytest

from smorest_sfs.modules.projects.models import Project


@pytest.mark.usefixtures("flask_app")
def test_project(temp_db_instance_helper: Callable[..., Iterator[Any]]) -> None:
    for project in temp_db_instance_helper(Project(name="test")):
        assert str(project) == "test"
