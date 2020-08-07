from typing import TYPE_CHECKING, Any, Dict, List, Set, Tuple, Type

import pytest
from _pytest.fixtures import SubRequest
from flask import Flask, url_for
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema

from tests._utils.client import AutoAuthFlaskClient

from .injection import FixturesInjectBase

if TYPE_CHECKING:
    from smorest_sfs.extensions.sqla import Model
    from smorest_sfs.modules.users.models import User


class Launcher(FixturesInjectBase):

    items: str
    listview: str
    listkeys: Set[str] = set(["id", "name"])
    view: str
    item_view: str
    login_roles: List[str]
    schema: Type[Schema]
    edit_param_key: str
    model: Type["Model"]

    flask_app_client: AutoAuthFlaskClient[Any]
    flask_app: Flask
    regular_user: "User"
    db: SQLAlchemy
    url: str

    def build_url(self, endpoint: str, **kwargs: Any) -> str:
        with self.flask_app.test_request_context():
            self.url = url_for(endpoint, **kwargs)
            return self.url

    def payload(self, method: str = "GET", **kwargs: Any) -> Response:
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                resp: Response = client.open(self.url, method=method, **kwargs)
                return resp


class ModifyLauncher(Launcher):
    @pytest.fixture(autouse=True)
    def auto_convert_schema(self, request: SubRequest) -> None:
        if hasattr(self, "schema") and isinstance(getattr(self, "schema"), str):
            setattr(self, "schema", request.getfixturevalue(getattr(self, "schema")))

    def _add_request(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        self.build_url(self.view, **kwargs)
        resp = self.payload("POST", json=data)

        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["code"] == 0
        )
        return resp.json["data"]

    def _get_deleting_items(self) -> Tuple[Any]:
        items: Tuple[Any] = getattr(self, self.items)
        return items[:1]

    def _get_modified_item(self) -> Any:
        items = getattr(self, self.items)
        return items[-1]

    def _delete_request(self, **kwargs: Any) -> Tuple[Any, Any]:
        self.build_url(self.view, **kwargs)
        items = self._get_deleting_items()
        ids = [i.id_ for i in items]
        resp = self.payload("DELETE", json={"lst": ids})
        assert (
            resp.status_code == 200
            and all([i.deleted for i in items])
            and resp.json["code"] == 0
        )
        return resp, items

    def _item_modify_request(
        self, json: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]:
        kwargs[self.edit_param_key] = self._get_modified_item().id_
        self.build_url(self.item_view, **kwargs)
        resp = self.payload("PUT", json=json)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["code"] == 0
        )
        return resp.json["data"]

    def _item_delete_request(self, **kwargs: Any) -> Tuple[Response, Any]:
        kwargs[self.edit_param_key] = self._get_modified_item().id_
        self.build_url(self.item_view, **kwargs)
        resp = self.payload("DELETE")
        item = self._get_modified_item()
        assert resp.status_code == 200 and item.deleted and resp.json["code"] == 0
        return resp, item

    def _validate_request(self, json: Dict[str, Any], **kwargs: Any) -> None:
        self.build_url(self.view, **kwargs)
        resp = self.payload("PUT", json=json)
        assert resp.status_code == 422


class AccessLauncher(Launcher):
    def _get_options(self, **kwargs: Any) -> Any:
        self.build_url(self.listview, **kwargs)
        resp = self.payload("GET")
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() == self.listkeys
            and resp.json["code"] == 0
        )
        return resp.json["data"]

    def _get_list(self, **kwargs: Any) -> List[Dict[str, Any]]:
        self.build_url(self.view, **kwargs)
        resp = self.payload("GET")
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["code"] == 0
        )
        return resp.json["data"]

    def _get_item(self, **kwargs: Any) -> Dict[str, Any]:
        self.build_url(self.item_view, **kwargs)
        resp = self.payload("GET")
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["code"] == 0
        )
        return resp.json["data"]
