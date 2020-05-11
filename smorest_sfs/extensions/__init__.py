#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    smorest_sfs.extensions
    ~~~~~~~~~~~~~~~~~~~~

    拓展组件
"""

from flask import Flask
from flask_babel import Babel
from flask_mail import Mail
from flask_migrate import Migrate

from .api import api, spec_kwargs
from .celery import Celery
from .jwt import jwt as jwt_instance
from .logger_helper import create_logger
from .marshal import ma
from .sqla import db
from .storage import redis_store

babel = Babel()
mail = Mail()
migrate = Migrate()
celery = Celery()

logger = create_logger()


def init_app(app: Flask) -> None:
    """拓展组件的初始化"""
    for ext in [db, ma, babel, mail, jwt_instance, redis_store, logger, celery]:
        ext.init_app(app)
    api.init_app(app, spec_kwargs=spec_kwargs)
    migrate.init_app(app, db)
