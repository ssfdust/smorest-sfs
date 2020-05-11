"""测试API"""
from typing import Any, Dict

import pytest
from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from flask_sqlalchemy import BaseQuery
from marshmallow import Schema

from smorest_sfs.extensions.api.decorators import paginate
from smorest_sfs.extensions.sqla import Model
from tests._utils.injection import FixturesInjectBase


class TestApi(FixturesInjectBase):
    TestPagination: Model
    TestPageSchema: Schema
    api: Api
    api_app: Flask

    fixture_names = ("api_app", "api", "TestPagination", "TestPageSchema")

    def setup_blp(self) -> None:
        blp = Blueprint("tests", "tests")

        TestPagination = self.TestPagination
        TestPageSchema = self.TestPageSchema

        class Pets(MethodView):  # pylint: disable=W0612
            @blp.response(TestPageSchema)
            @paginate()
            def get(self) -> BaseQuery:
                """List pets"""
                query: BaseQuery = TestPagination.query.order_by(TestPagination.id)
                return query

        blp.add_url_rule("", "pets", Pets.as_view("pets"))

        self.api.register_blueprint(blp, base_prefix="/pets", url_prefix="/")

    @pytest.mark.parametrize(
        "meta",
        [
            (
                {
                    "links": {
                        "first": "/pets/?page=1&per_page=5",
                        "last": "/pets/?page=4&per_page=5",
                        "next": "/pets/?page=3&per_page=5",
                        "prev": "/pets/?page=1&per_page=5",
                    },
                    "page": 2,
                    "pages": 4,
                    "per_page": 5,
                    "total": 20,
                }
            )
        ],
    )
    def test_api(self, meta: Dict[str, Any]) -> None:
        # pylint: disable=W0613
        self.setup_blp()
        data = self.get_test_json("pets/?page=2&per_page=5")

        assert data["meta"] == meta

    def get_test_json(self, url: str) -> Dict[str, Any]:
        test_client = self.api_app.test_client()
        resp = test_client.get(url)
        json: Dict[str, Any] = resp.json
        return json
