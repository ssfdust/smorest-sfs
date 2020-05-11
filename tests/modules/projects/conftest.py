#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from flask import Flask
from marshmallow import Schema

from smorest_sfs.modules.projects.models import Project


@pytest.fixture
def project_items(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Project, Project, Project]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(
        *(Project(name=str(_) + "tqwq") for _ in range(3))
    ):
        yield _


@pytest.fixture
def ProjectSchema(flask_app: Flask) -> Type[Schema]:
    # pylint: disable=W0621, W0613
    from smorest_sfs.modules.projects.schemas import ProjectSchema
    return ProjectSchema