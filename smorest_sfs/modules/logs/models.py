"""
    smorest_sfs.modules.logs.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    日志的ORM模块
"""
from sqlalchemy_utils.types import JSONType

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db


class Log(Model, SurrogatePK):
    """
    日志

    :attr module: str(128) 请求模块
    :attr line: int 行
    :attr level 日志等级
    :attr message 日志消息
    """

    __tablename__ = "logs"

    module = db.Column(db.String(length=128), nullable=False, doc="请求模块")
    line = db.Column(
        db.Integer, nullable=False, doc="行", info={"marshmallow": {"dump_only": True}}
    )
    level = db.Column(db.String(length=20), nullable=False, doc="日志等级")
    message = db.Column(
        db.TEXT, nullable=False, doc="日志消息", info={"marshmallow": {"dump_only": True}}
    )

    def __repr__(self) -> str:
        return self.message[:20]


class ResponseLog(Model, SurrogatePK):
    """
    请求日志

    :attr url: str(4096) url地址
    :attr arguments: json 请求数据
    :attr method: str(10) 请求方法
    :attr ip: str(128) IP地址
    :attr module: str(128) 模块名
    :attr status_code: int 状态码
    """

    url = db.Column(db.String(4096), nullable=False, doc="请求url")
    arguments = db.Column(JSONType, doc="请求数据")
    method = db.Column(db.String(10), nullable=False, doc="请求方法")
    ip = db.Column(db.String(128), doc="IP地址")
    module = db.Column(db.String(128), doc="模块名")
    status_code = db.Column(db.Integer, doc="状态码")

    def __repr__(self) -> str:
        return "{} {}".format(self.method, self.url[0:20])
