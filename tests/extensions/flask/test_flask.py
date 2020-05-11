#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试自定义的Flask"""

import tempfile

from smorest_sfs.extensions.flask import Flask


class TestFlask:
    def test_flask(self) -> None:

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(b"TEST_CONFIG = 123")

        app = Flask("TestFlask")
        app.config.from_toml(fp.name)

        assert app.config["TEST_CONFIG"] == 123
