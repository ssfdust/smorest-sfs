#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Dict, Protocol

import pytest

from smorest_sfs.services.mail import PasswdMailSender
from tests._utils.injection import UniqueQueue


class MsgProtocol(Protocol):
    html: str


SENDED: UniqueQueue[MsgProtocol] = UniqueQueue()


def fake_send(msg: Any) -> None:
    SENDED.put(msg)


@pytest.fixture
def patched_send_mail(monkeypatch: Any) -> None:
    from smorest_sfs.extensions import mail

    monkeypatch.setattr(mail, "send", fake_send)


class TestSendMail:
    @pytest.mark.parametrize(
        "content, result",
        [
            (
                {"message": "这是一个测试", "url": "testing-reset-password"},
                '<p>这是一个测试</p><a href="testing-reset-password" target="_blank">点击访问</a>',
            )
        ],
    )
    @pytest.mark.usefixtures("patched_send_mail")
    def test_send_mail(self, content: Dict[str, str], result: str) -> None:
        sender = PasswdMailSender(content, "test@test.com")
        sender.send()
        msg = SENDED.get()
        assert msg.html == result
