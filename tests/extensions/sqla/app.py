import os

import toml
from flask import Flask
from flask_babel import Babel

from smorest_sfs.extensions.sqla.db_instance import BaseModel
from smorest_sfs.extensions.sqla.db_instance import db as sqla_db
from smorest_sfs.extensions.sqla.surrogatepk import SurrogatePK
from smorest_sfs.utils.paths import ProjectPath


def get_pg_uri() -> str:
    test_config_path = ProjectPath.get_subpath_from_project("config/testing.toml")
    try:
        path: str = toml.load(test_config_path)["SQLALCHEMY_DATABASE_URI"]
        return path
    except (FileNotFoundError, KeyError):
        return os.environ.get("PG_URI", "postgresql://postgres@localhost/postgres")


def create_app() -> Flask:
    flask_app = Flask("TestSqla")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = get_pg_uri()
    flask_app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Shanghai"
    flask_app.config["TESTING"] = True
    Babel(flask_app)

    return flask_app


flask_app = create_app()
sqla_db.init_app(flask_app)


class TestCRUDTable(SurrogatePK, BaseModel):
    __tablename__ = "sqla_test_crud_table"

    name = sqla_db.Column(sqla_db.String(80), unique=True)
