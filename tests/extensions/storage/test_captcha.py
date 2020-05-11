"""测试验证码"""
import pytest
from flask import Flask
from werkzeug.exceptions import NotFound

from smorest_sfs.extensions import redis_store
from smorest_sfs.extensions.storage.captcha import CaptchaStore


class TestCapture:
    @pytest.mark.parametrize("key", [("test1"), ("test2"), ("test1")])
    def test_save_restore_capture(self, key: str, captcha_app: Flask) -> None:
        redis_store.init_app(captcha_app)
        store = CaptchaStore(key)
        value = store.generate_captcha()
        store = CaptchaStore(key)
        assert store.verify(value) is True

    def test_empty(self, captcha_app: Flask) -> None:
        redis_store.init_app(captcha_app)
        store = CaptchaStore("unkown")
        with pytest.raises(NotFound):
            store.verify("unkown")
