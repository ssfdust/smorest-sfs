"""
    app.extensions.marshal.fields
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    自定义的Marshmallow Filed模块
"""

from typing import Any, Union

import pendulum
from flask_babel import get_timezone
from marshmallow import fields

from smorest_sfs.utils.datetime import convert_timezone, datetime


class PendulumField(fields.DateTime):
    """
    Pendulumn类型字段

    主要用以结合flask-babel模块处理时区问题，返回后以Pendulumn类型
    """

    def _deserialize(
        self, value: str, attr: Any, data: Any, **kwargs: Any
    ) -> pendulum.DateTime:
        """反序列化"""
        if not value:
            raise self.make_error("invalid", input=value, obj_type=self.OBJ_TYPE)

        timezone = get_timezone()
        dt: pendulum.DateTime = pendulum.parse(value, tz=timezone)  # type: ignore
        return convert_timezone(dt, "utc")

    def _serialize(
        self, value: Union[None, datetime.datetime], attr: Any, obj: Any, **kwargs: Any
    ) -> Any:
        """序列化"""
        if value is None:
            return value
        timezone = str(get_timezone())
        value = convert_timezone(pendulum.instance(value), timezone)
        return super()._serialize(value, attr, obj, **kwargs)  # type: ignore
