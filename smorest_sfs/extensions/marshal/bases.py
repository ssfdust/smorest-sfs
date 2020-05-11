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
    app.extensions.marshal.bases
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    项目中常用的基本结构

    这个模块包含最基本的返回结构，比如基本分页，基本消息
    此项目中常用的基本格式为：
    {
        "code": 0,
        "msg": "消息内容",
        "data": data
    }
"""
from typing import Any, Dict

from marshmallow import Schema, fields, post_load

from smorest_sfs.utils.datetime import expand_datetime

from .fields import PendulumField


class BaseMsgSchema(Schema):
    """基本消息格式"""

    msg = fields.Str(description="消息", default="success")
    code = fields.Int(description="状态码", default="0")


class BaseIntListSchema(Schema):
    """基本json列表格式"""

    lst = fields.List(fields.Int, missing=[], description="数字列表")


class LinkMetaSchema(Schema):
    """基本分页链接格式"""

    next = fields.Str(description="下一页url")
    prev = fields.Str(description="前一页url")
    first = fields.Str(description="首页url")
    last = fields.Str(description="尾页url")


class PageMetaSchema(Schema):
    """基本分页页码格式"""

    page = fields.Integer(description="页码")
    per_page = fields.Integer(description="每页数量")
    total = fields.Integer(description="总数")
    pages = fields.Integer(description="总页数")
    links = fields.Nested(LinkMetaSchema)


class BasePageSchema(Schema):
    """基本分页格式"""

    msg = fields.Str(description="消息", default="success")
    meta = fields.Nested(PageMetaSchema, description="分页Meta信息")
    code = fields.Int(description="状态码", default="0")


class UploadField(fields.Field):
    """文件提交栏，复用Field类型"""


class GeneralParam(Schema):
    """统一模糊查询"""

    name__contains = fields.Str(description="名称", data_key="name")


class BaseTimeParam(Schema):
    """
    常用的参数序列化类
    """

    created__between = PendulumField(
        data_key="created_date", description="创建日期", load_only=True
    )
    modified__between = PendulumField(
        data_key="modified_date", description="修改日期", load_only=True
    )
    created__ge = PendulumField(description="晚于创建时间", load_only=True)
    created__le = PendulumField(description="早于创建时间", load_only=True)
    modified__ge = PendulumField(description="晚于修改时间", load_only=True)
    modified__le = PendulumField(description="早于修改时间", load_only=True)

    @post_load
    def expand_to_range(self, data: Dict[str, Any], **_: Any) -> Dict[str, Any]:
        for key in ["created__between", "modified__between"]:
            try:
                data[key] = expand_datetime(data[key])
            except KeyError:
                continue
        return data
