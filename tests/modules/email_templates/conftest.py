#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from flask import Flask
from marshmallow import Schema

from smorest_sfs.modules.email_templates.models import EmailTemplate


@pytest.fixture
def email_template_items(
    flask_app: Flask, temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[EmailTemplate, EmailTemplate, EmailTemplate]]:
    # pylint: disable=W0613
    for _ in temp_db_instance_helper(
        *(EmailTemplate(name=str(_), template="qq") for _ in range(3))
    ):
        yield _


@pytest.fixture
def EmailTemplateSchema(flask_app: Flask) -> Type[Schema]:
    # pylint: disable=W0621, W0613
    from smorest_sfs.modules.email_templates.schemas import EmailTemplateSchema

    return EmailTemplateSchema
