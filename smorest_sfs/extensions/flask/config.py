"""
    app.extensions.config
    ~~~~~~~~~~~~~~~~~~~~~~~~

    config模块

    源自：Flask-Environment
    由于pytoml已经不再支持以及源码不长故在重新在本地实现

    使用：
    >>> from flask import Flask as BaseFlask
    >>> from app.config import Config
    >>> class Flask(BaseFlask):
            config_class = Config
    >>> app = Flask('test')
    >>> app.config.from_toml('/path/to/toml_file')
"""

import os

import toml
from flask.config import Config as FlaskConfig


class Config(FlaskConfig):
    """支持from_toml的config模块"""

    def from_toml(self, filename: str) -> bool:
        """从TOML文件中更新配置中的值。就好像TOML对象是一个字典，并传递到
        """

        # Prepeend the root path is we don't have an absolute path
        filename = (
            os.path.join(self.root_path, filename)
            if filename.startswith(os.sep)
            else filename
        )

        try:
            with open(filename) as toml_file:
                obj = toml.load(toml_file)
        except IOError as e:
            e.strerror = "Unable to load configuration file (%s)" % e.strerror
            raise

        return self.from_mapping(obj) is True
