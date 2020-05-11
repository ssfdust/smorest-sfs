#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import secrets
import string
import sys
from itertools import chain
from typing import Dict

from tasks.app._utils import rlinput
from tasks.app.consts import CONFIG_PATH

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

try:
    import toml
    from sqlalchemy.engine import url
    from kombu.utils.url import parse_url
except ImportError as e:
    log.critical("缺少%s模块，请通过`pip install %s`安装", e.name, e.name)
    sys.exit(1)

SETTING_KEYS = {
    "MODULE_BASE_PREFIX",
    "SQLALCHEMY_DATABASE_URI",
    "CELERY_BROKER_URL",
    "CELERY_REDIS_BACKEND_URL",
    "AMQP_URL",
    "BABEL_DEFAULT_TIMEZONE",
    "BABEL_DEFAULT_LOCALE",
    "MAIL_SERVER",
    "MAIL_PORT",
    "MAIL_USERNAME",
    "MAIL_DEFAULT_SENDER",
    "MAIL_PASSWORD",
}

RANDOM_KEYS = {"JWT_SECRET_KEY"}

HELPS = {
    "SQLALCHEMY_DATABASE_URI": "Postgresql数据库连接地址(SQLAlchemy地址)",
    "BABEL_DEFAULT_LOCALE": "本地化字符串",
    "MODULE_BASE_PREFIX": "url默认前缀",
    "BABEL_DEFAULT_TIMEZONE": "时区",
    "MAIL_SERVER": "邮箱服务地址",
    "MAIL_USERNAME": "邮箱登录用户名",
    "MAIL_PASSWORD": "邮箱登录密码",
    "MAIL_DEFAULT_SENDER": "发件人",
    "MAIL_PORT": "邮箱服务端口",
    "CELERY_BROKER_URL": "celery broker地址",
    "CELERY_REDIS_BACKEND_URL": "celery redis地址",
    "AMQP_URL": "amqp地址",
    "JWT_SECRET_KEY": "JWT用的密钥字符串",
}


def rand_string(strlen=10):
    """生成数字字母特殊字符的随机字符串"""
    password_characters = (
        string.ascii_letters + string.digits + string.punctuation.replace("'", "")
    )
    return "".join(
        secrets.choice(password_characters) for i in range(strlen) if i != "'"
    )


class _Config:

    default_config = {
        "SQLALCHEMY_DATABASE_URI": "postgresql://root:root@localhost/mydb",
        "BABEL_DEFAULT_LOCALE": "zh_cn",
        "MODULE_BASE_PREFIX": "/api/v1",
        "BABEL_DEFAULT_TIMEZONE": "Asia/Shanghai",
        "MAIL_SERVER": "smtp.exmail.qq.com",
        "MAIL_PORT": "465",
        "CELERY_BROKER_URL": "amqp://",
        "CELERY_REDIS_BACKEND_URL": "redis://",
        "AMQP_URL": "amqp://",
    }
    development_config = {}
    production_config = {}
    testing_config = {}
    _setting_keys = sorted(list(SETTING_KEYS))
    _random_keys = sorted(list(RANDOM_KEYS))
    current_type = ""

    def __init__(self, configdir=None):
        self.configdir = configdir

    @property
    def config_types(self):
        return {
            "development": self.development_config,
            "production": self.production_config,
            "testing": self.testing_config,
        }

    def set_configurations(self):
        for config_type, config in self.config_types.items():
            self.current_type = config_type
            log.info("正在为%s环境设置配置....", config_type)
            self._set_key_values(config)
            self._parse_config(config)
            self._update_default_config()

    def _set_key_values(self, config: Dict):
        for key in chain(self._setting_keys, self._random_keys):
            self._update_config_for(key, config)

    def _update_config_for(self, key: str, config: Dict):
        default = (
            "{}-testing".format(self._get_default_for(key))
            if self.current_type == "testing" and key == "SQLALCHEMY_DATABASE_URI"
            else self._get_default_for(key)
        )
        prompt = "请设置 %s (%s) \n(默认 %s): \n" % (key, HELPS[key], default)
        config[key] = rlinput(prompt, default)
        print()

    def _update_default_config(self):
        if self.default_config != self.development_config:
            self.default_config.update(self.development_config)
            self._setting_keys = set(
                key
                for key in self.default_config
                if key not in ["DB_URL_INFO", "BROKER_URL_INFO"]
            )
            self._random_keys = set(self._random_keys) - set(self._setting_keys)

    def _get_default_for(self, key: str):
        try:
            return self.development_config[key]
        except KeyError:
            if key in self._random_keys:
                return rand_string(30)
            return self.default_config.get(key, "")


class _ConfigLoader:
    def load_configurations(self):
        for config_type, config in self.config_types:
            if not config:
                config = toml.load(CONFIG_PATH.format(config_type))
                self._parse_config(config)
        return self

    @staticmethod
    def _parse_config(config: Dict):
        db_url = url.make_url(config["SQLALCHEMY_DATABASE_URI"])
        broker_url = parse_url(config["CELERY_BROKER_URL"])
        config["DB_URL_INFO"] = {
            "username": db_url.username,
            "password": db_url.password,
            "database": db_url.database,
            "host": db_url.host,
            "port": db_url.port,
        }
        config["BROKER_URL_INFO"] = {
            "username": broker_url["userid"],
            "password": broker_url["password"],
        }


class Config(_Config, _ConfigLoader):
    pass
