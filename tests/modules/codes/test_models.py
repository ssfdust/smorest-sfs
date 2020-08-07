#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


@pytest.mark.usefixtures("flask_app", "fake_codes")
def test_simple_code() -> None:
    from smorest_sfs.modules.codes.models import Code

    codes = Code.where(type_code="test-001").all()
    assert {"A001", "B001", "C001"} == {code.name for code in codes}


@pytest.mark.usefixtures("flask_app", "fake_codes")
def test_simple_notnull() -> None:
    from smorest_sfs.modules.codes.models import Code

    null_codes = Code.where(type_code__isnull=True).all()
    assert len(null_codes) == 0
