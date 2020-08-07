#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest
from _pytest.monkeypatch import MonkeyPatch

from tests._utils.uniqueue import UniqueQueue

QUEUE: UniqueQueue[str] = UniqueQueue()
MODEL_NAME = "smorest_sfs.modules.users.models.User"
SCHEMA_NAME = "smorest_sfs.modules.users.schemas.UserSchema"


@pytest.mark.usefixtures("flask_app", "inject_logger")
def test_invaild_module_loads(monkeypatch: MonkeyPatch) -> None:
    from smorest_sfs.modules import auth, load_module
    from smorest_sfs.extensions.sqla import db, Model
    from smorest_sfs.plugins.samanager import SqlaManager
    from smorest_sfs.modules.users.models import User
    from smorest_sfs.modules.users.schemas import UserSchema

    manager: SqlaManager[Model] = SqlaManager(db.session)

    monkeypatch.setattr(auth, "preload_modules", ["ttt"])
    monkeypatch.setattr(auth, "ma_mapping", {MODEL_NAME: SCHEMA_NAME})
    load_module("auth")
    assert (
        QUEUE.get()
        == "无法加载{module_name}下的{submodule}".format(module_name="auth", submodule="ttt")
        and SqlaManager.get_mappings()
    ) and manager.get_mappings()[User] == UserSchema
