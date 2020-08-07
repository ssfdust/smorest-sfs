#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import uuid
from typing import TYPE_CHECKING, Any, Iterator, List, Union

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
from mixer.backend.marshmallow import Mixer as MaMixer
from mixer.backend.marshmallow import NestedMixer
from mixer.backend.sqlalchemy import Mixer as SqlaMixer

from ._utils import clear, client, injection, tables, users
from .config import pytest_plugins as _pytest_plugins
from .typings import INS_HELPER, M

if TYPE_CHECKING:
    from smorest_sfs.modules.users.models import User


class fakeuuid:
    hex = "123456789"


pytest_plugins = _pytest_plugins


@pytest.fixture
def patch_uuid(monkeypatch: Any) -> None:
    monkeypatch.setattr(uuid, "uuid4", fakeuuid)


@pytest.fixture
def clean_dirs() -> Iterator[None]:
    from smorest_sfs.utils.paths import UploadPath

    yield
    for key in ["foo", "new", "bar"]:
        path = UploadPath.get_uploads_subdir(key, withdate=False)
        if path.exists():
            shutil.rmtree(path)


@pytest.fixture(scope="session")
def flask_app() -> Iterator[Flask]:
    # pylint: disable=W0613, W0621
    from migrations.initial_data import (
        init_email_templates,
        init_groups,
        init_permission,
    )

    os.environ["FLASK_ENV"] = "testing"
    from smorest_sfs.app import app
    from smorest_sfs.extensions import db
    from smorest_sfs.extensions.sqla.db_instance import BaseModel

    clear.clear_dummy(app)
    BaseModel.set_session(db.session)

    with app.app_context():
        db.create_all()
        init_permission()
        init_groups()
        init_email_templates()
        db.session.commit()
        yield app

        db.drop_all()


@pytest.yield_fixture(scope="session")
def db(flask_app: Flask) -> Iterator[SQLAlchemy]:
    # pylint: disable=W0613, W0621
    from smorest_sfs.extensions import db as db_instance

    yield db_instance


@pytest.fixture(scope="session")
def flask_app_client(flask_app: Flask) -> client.FlaskClient[Any]:
    # pylint: disable=W0613, W0621
    flask_app.test_client_class = client.AutoAuthFlaskClient[Any]
    return flask_app.test_client()


@pytest.fixture(scope="session")
def temp_db_instance_helper(db: SQLAlchemy) -> INS_HELPER[M]:
    def temp_db_instance_manager(*instances: M,) -> Iterator[Union[M, List[M]]]:
        for instance in instances:
            db.session.add(instance)

        if len(instances) == 1:
            yield instances[0]
        else:
            yield list(instances)

        tables.clear_instances(db, instances)
        db.session.commit()

    return temp_db_instance_manager


@pytest.fixture(scope="session")
def regular_user(temp_db_instance_helper: INS_HELPER["User"]) -> Iterator["User"]:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="regular_user")
    ):
        yield _


@pytest.fixture(scope="session")
def inactive_user(temp_db_instance_helper: INS_HELPER["User"]) -> Iterator["User"]:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="inactive_user", phonenum="inactive_user")
    ):
        yield _


def pytest_pyfunc_call(pyfuncitem: Any) -> None:
    from smorest_sfs.extensions import db

    try:
        if "modules" in pyfuncitem.location[0]:
            db.session.commit()
    except RuntimeError:
        pass


@pytest.fixture(scope="session")
def forget_passwd_user(temp_db_instance_helper: INS_HELPER["User"]) -> Iterator["User"]:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(
            username="forget_passwd_user", phonenum="forget_passwd_user"
        )
    ):
        yield _


@pytest.fixture(scope="session")
def guest_user(temp_db_instance_helper: INS_HELPER["User"]) -> Iterator["User"]:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="guest_user", phonenum="guest_user")
    ):
        yield _


@pytest.fixture
def inject_logger() -> Iterator[None]:
    logger_id = injection.inject_logger(logger)
    yield
    injection.uninject_logger(logger, logger_id)


@pytest.fixture(scope="session")
def sqla_mixer(flask_app: Flask, db: SQLAlchemy) -> SqlaMixer:
    return SqlaMixer(session=db.session, commit=False)


@pytest.fixture(scope="session")
def ma_mixer(flask_app: Flask) -> MaMixer:
    return MaMixer(required=True)


@pytest.fixture(scope="session")
def nested_mixer(flask_app: Flask) -> NestedMixer:
    return NestedMixer(required=True)
