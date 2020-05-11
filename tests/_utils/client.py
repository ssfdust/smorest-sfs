#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Iterator, List, Optional, TypeVar, Union

from flask import testing

from smorest_sfs.modules.users.models import User

_R = TypeVar("_R")

if TYPE_CHECKING:
    FlaskClient = testing.FlaskClient
else:

    class FakeGenericMeta(type):
        def __getitem__(self, item):
            return self

    class FlaskClient(testing.FlaskClient, metaclass=FakeGenericMeta):
        pass


#  class JSONResponse(Response):
#      """
#      A Response class with extra useful helpers, i.e. ``.json`` property.
#
#      来源：https://github.com/frol/flask-restplus-server-example/
#      """
#
#      # pylint: disable=too-many-ancestors
#
#      @cached_property
#      def json(self) -> JSONMixin:
#          return json.loads(self.get_data(as_text=True), object_pairs_hook=dict)
#
#
class AutoAuthFlaskClient(FlaskClient[_R]):
    """
    A helper FlaskClient class with a useful for testing ``login`` context
    manager.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super(AutoAuthFlaskClient, self).__init__(*args, **kwargs)
        self._user: Union[User, None] = None
        self._access_token: Union[str, None] = None
        self._roles: List[str] = []

    @contextmanager
    def login(
        self, user: User, roles: Optional[List[str]] = None
    ) -> Iterator[AutoAuthFlaskClient[Any]]:
        """
        示例：
            >>> with flask_app_client.login(user, permissions=['SuperUserPrivilege']):
            ...     flask_app_client.get('/api/v1/users/')
        """
        from smorest_sfs.services.auth.auth import login_user, logout_user
        from smorest_sfs.modules.roles.models import Role

        self._user = user
        self._roles = roles or []
        self._user.roles = Role.where(name__in=self._roles).all()
        self._user.save()
        if self._user is not None:
            self._access_token = login_user(self._user)["tokens"]["access_token"]
        yield self
        logout_user(self._user)
        self._user.roles = []
        self._user.save()
        self._user = None

    def open(self, *args: str, **kwargs: Any) -> Any:
        if self._access_token is not None:
            kwargs = self._combine_headers(**kwargs)

        response = super(AutoAuthFlaskClient, self).open(*args, **kwargs)

        return response

    def _combine_headers(self, **kwargs: Any) -> Any:
        extra_headers = (
            ("Authorization", "Bearer {token}".format(token=self._access_token)),
        )
        if kwargs.get("headers"):
            kwargs["headers"] += extra_headers
        else:
            kwargs["headers"] = extra_headers
        return kwargs
