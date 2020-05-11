# Copyright 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    smorest_sfs.extensions.logger
    ~~~~~~~~~~~~~~~~~~~~~~

    日志处理模块，打印日志同时保存到MongoDb
"""
from datetime import datetime
from typing import Any, Dict, Optional, Protocol, Type

from flask import Flask, Response, request
from loguru import logger


class Publisher(Protocol):
    def __init__(self, *args: Any, **kwargs: Any):
        # pylint: disable=W0231
        ...  # pragma: no cover

    def publish(self, item: Any) -> None:
        ...  # pragma: no cover


def _parse_args(resp: Response) -> Dict[str, Any]:
    if request.method == "GET":
        return request.args.to_dict()
    return resp.json


def _parse_ip() -> str:
    nginx_remote = "X-Forwarded-For"
    return (
        request.headers[nginx_remote]
        if nginx_remote in request.headers
        else request.remote_addr
    )


class Logger:
    """
    日志处理
    """

    publisher: Publisher
    handler_id: int

    def __init__(
        self, publish_cls: Type[Publisher], app: Optional[Flask] = None, **kwargs: Any
    ):
        self._app = app
        self.publisher_args = kwargs.get("publish_args", {})
        self.publisher_cls = publish_cls
        if self._app:
            self.init_app(self._app)

    def init_app(self, app: Flask) -> None:
        self._app = app
        self._app.after_request(self.save_resp)
        self._app.extensions["logger_ext"] = self
        self.handler_id = logger.add(self.handle_record)

    def check_publisher(self) -> None:
        if not hasattr(self, "publisher"):
            self.publisher = self.publisher_cls(**self.publisher_args)

    def save_resp(self, resp: Response) -> Response:
        """保存Request请求"""
        self.check_publisher()
        args = _parse_args(resp)
        data = dict(
            created=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            log_type="response",
            url=request.path,
            arguments=args,
            method=request.method,
            ip=_parse_ip(),
            module=request.endpoint if request.endpoint else "unknown",
            status_code=resp.status_code,
        )
        self.publisher.publish(data)
        return resp

    def handle_record(self, message: Any) -> None:
        """处理来自loguru的信息"""
        self.check_publisher()
        data = dict(
            log_type="logging",
            created=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            module=message.record["name"],
            line=message.record["line"],
            level=message.record["level"].name,
            message=str(message.record["message"]),
        )
        self.publisher.publish(data)
