"""
    smorest_sfs.factory
    ~~~~~~~~~~~~~~~~~~~~~
    工厂模块

    用以提供库的初始化函数以及注册模块
"""
import os
from typing import List

from . import errors, modules
from .extensions import init_app
from .extensions.flask import Flask

CONFIG_MAPPGING = {
    "development": "config/development.toml",
    "production": "config/production.toml",
    "testing": "config/testing.toml",
}


def create_app(module_names: List[str], config_name: str = "development") -> Flask:
    """
    创建app工厂

    :param modules 启用模块列表
    :param config_name 配置名称

    ```modules``` 启用的模块列表，模块名必须在app.modules下存在，
    将会按照顺序导入模块。

    ```config_name``` 配置名称，启用的配置名称，存在development,
    production, testing三种配置，从app/config下引用对应的TOML
    配置文件，默认是development配置。
    通过环境变量export FLASK_ENV可以覆盖掉默认的配置信息，在Docker中
    比较好用。
    """
    app = Flask("Smart-Smorest")

    config_type = os.environ.get("FLASK_ENV", config_name)

    app.config.from_toml(CONFIG_MAPPGING[config_type])

    app.config["ENABLED_MODULES"] = module_names

    init_app(app)

    register_modules(app)

    return app


def register_modules(app: Flask) -> None:
    """
    注册模块

    为Flask实例注册项目的主要模块
    """
    modules.init_app(app)
    errors.init_app(app)
