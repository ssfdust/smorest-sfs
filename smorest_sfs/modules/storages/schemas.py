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

from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal.bases import BaseMsgSchema, UploadField


class UploadParams(Schema):
    """
    上传参数
    """

    file = UploadField(description="文件", allow_none=False, required=True)


class StoragesSchema(Schema):

    file_id = fields.Int()


class UploadSchema(BaseMsgSchema):
    data = fields.Nested(StoragesSchema)
