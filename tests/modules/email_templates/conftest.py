from typing import Dict

import pytest
from flask import Flask
from mixer.backend.marshmallow import NestedMixer


@pytest.fixture
def email_template_args(flask_app: Flask, nested_mixer: NestedMixer) -> Dict[str, str]:
    from smorest_sfs.modules.email_templates.schemas import EmailTemplateSchema

    data: Dict[str, str] = nested_mixer.blend(EmailTemplateSchema)

    return data
