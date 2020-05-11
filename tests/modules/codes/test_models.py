#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.codes.models import Code


@pytest.mark.usefixtures("flask_app", "fake_codes")
def test_simple_code() -> None:
    codes = Code.where(type_code="test-001").all()
    assert {"A001", "B001", "C001"} == {code.name for code in codes}
