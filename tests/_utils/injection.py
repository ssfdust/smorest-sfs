#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Any, Dict, List, Set, Tuple, Type, Union

import pytest
from _pytest.fixtures import SubRequest
from flask import Flask, url_for
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema

from smorest_sfs.extensions.sqla import Model
from smorest_sfs.modules.email_templates.models import EmailTemplate
from smorest_sfs.modules.projects.models import Project
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import User
from tests._utils.client import AutoAuthFlaskClient

from .uniqueue import UniqueQueue

if TYPE_CHECKING:
    from loguru import Message
    from loguru import Logger
else:
    from loguru._handler import Message
    from loguru._logger import Logger


def log_to_queue(record: Message) -> None:
    queue: UniqueQueue[str] = UniqueQueue()
    queue.put(record.record["message"])


def inject_logger(logger: Logger) -> int:
    return logger.add(log_to_queue, serialize=False)


def uninject_logger(logger: Logger, logger_id: int) -> None:
    logger.remove(logger_id)


class FixturesInjectBase:

    items: str
    listview: str
    listkeys: Set[str] = {"id", "name"}
    view: str
    item_view: str
    login_roles: List[str]
    model: Type[Model]
    schema: Union[Type[Schema], str]
    delete_param_key: str
    fixture_names: Tuple[str, ...] = tuple()

    flask_app_client: AutoAuthFlaskClient[Any]
    flask_app: Flask
    regular_user: User
    db: SQLAlchemy

    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request: SubRequest) -> None:  # type: ignore
        names = self.fixture_names
        for name in names:
            setattr(self, name, request.getfixturevalue(name))


class GeneralModify(FixturesInjectBase):
    @pytest.fixture(autouse=True)
    def auto_convert_schema(self, request: SubRequest) -> None:
        if hasattr(self, "schema") and isinstance(getattr(self, "schema"), str):
            setattr(self, "schema", request.getfixturevalue(getattr(self, "schema")))

    def _add_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(self.view)
                resp = client.post(url, json=data)
                item = self.model.get_by_id(resp.json["data"]["id"])
                dumped_data = self.__dump_item_from_schema(item)
                self.model.where(id=resp.json["data"]["id"]).delete()
                self.db.session.commit()
                assert resp.status_code == 200 and isinstance(resp.json["data"], dict)
                return dumped_data

    def _get_deleting_items(self) -> Tuple[Any]:
        items: Tuple[Any] = getattr(self, self.items)
        return items[:1]

    def _get_modified_item(self) -> Any:
        items = getattr(self, self.items)
        return items[-1]

    def __dump_item_from_schema(self, item: Any) -> Dict[str, Any]:
        if isinstance(self.schema, str):
            raise RuntimeError(f"Schema {self.schema} fixture doesn't defined")
        schema = self.schema()
        return self.__get_schema_dumped(schema, item)

    @staticmethod
    def __get_schema_dumped(schema: Schema, item: Any,) -> Dict[str, Any]:
        dumpd: Dict[str, Any] = schema.dump(item)
        return dumpd

    def _get_dumped_modified_item(self) -> Dict[str, Any]:
        item = self._get_modified_item()
        return self.__dump_item_from_schema(item)

    def _delete_request(
        self,
    ) -> Tuple[Any, Tuple[Union[EmailTemplate, Project, Role]]]:
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(self.view)
                items = self._get_deleting_items()
                ids = [i.id for i in items]
                resp = client.delete(url, json={"lst": ids})
                assert resp.status_code == 200 and all([i.deleted for i in items])
                return resp, items

    def __item_modify_request(self, method: str, **kwargs: Any) -> Any:
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                item = self._get_modified_item()
                url = url_for(self.item_view, **{self.delete_param_key: item.id})
                resp = client.open(url, method=method, **kwargs)
                return resp

    def _item_modify_request(self, json: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.__item_modify_request("PUT", json=json)
        if isinstance(self.schema, str):
            raise RuntimeError()
        schema = self.schema()
        item = self._get_modified_item()
        dumped_data = self.__get_schema_dumped(schema, item)
        assert resp.status_code == 200
        return dumped_data

    def _item_delete_request(self,) -> Tuple[Response, Any]:
        resp = self.__item_modify_request("DELETE")
        item = self._get_modified_item()
        assert resp.status_code == 200 and item.deleted
        return resp, item


class GeneralGet(FixturesInjectBase):
    def _get_view(self, endpoint: str, **kwargs: Any) -> Any:
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(endpoint, **kwargs)
                return client.get(url)

    def _get_options(self, **kwargs: Any) -> Any:
        resp = self._get_view(self.listview, **kwargs)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() == self.listkeys
        )
        return resp.json["data"]

    def _get_list(self, **kwargs: Any) -> List[Dict[str, Any]]:
        resp = self._get_view(self.view, **kwargs)
        assert resp.status_code == 200 and isinstance(resp.json["data"], list)
        return resp.json["data"]

    def _get_item(self, **kwargs: Any) -> Dict[str, Any]:
        resp = self._get_view(self.item_view, **kwargs)
        assert resp.status_code == 200 and isinstance(resp.json["data"], dict)
        return resp.json["data"]
