"""
    smorest_sfs.extensions.flask
    ~~~~~~~~~~~~~~~~~~~~~

    拓展的Flask类
"""

from flask import Flask as BaseFlask

from .config import Config


class Flask(BaseFlask):
    """
    支持from_toml的Flask类
    """

    config: Config
    config_class = Config
