#!/usr/bin/env python
# -*- coding: utf-8 -*-
import secrets
import string
from typing import Optional

from werkzeug.exceptions import NotFound

from . import redis_store


class CaptchaStore:
    def __init__(self, token: str):
        self.token = token
        self.key = f"capture_{token}"
        self._code: Optional[str] = None

    def generate_captcha(self, length: int = 4) -> str:
        passwd_str = string.digits + string.ascii_letters
        code = "".join([secrets.choice(passwd_str) for i in range(length)])
        return self._set_code(code)

    def _set_code(self, code: str) -> str:
        redis_store.set(self.key, code.lower())
        return code

    def verify(self, value: str) -> bool:
        if value.lower() != self._get_values():
            raise ValueError("验证码错误")
        return True

    def _get_values(self) -> Optional[str]:
        if self._code is None:
            code = redis_store.get(self.key)
            self._decode_code(code)
            redis_store.delete(self.key)
        return self._code

    def _decode_code(self, code: Optional[bytes]) -> None:
        if code:
            self._code = code.decode("utf-8")
        else:
            raise NotFound
