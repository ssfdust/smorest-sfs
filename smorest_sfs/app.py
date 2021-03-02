"""
    smorest_sfs.app
    ~~~~~~~~~~~~~~~~~~~~~~
    实例模块
"""

from .extensions import celery
from .factory import create_app

ENABLED_MODULES = [
    "auth",
    "storages",
    "roles",
    "users",
    "groups",
    "email_templates",
    "codes",
    "menus",
    "logs",
    "projects",
]


app = create_app(ENABLED_MODULES)
celery_app = celery.get_celery_app()
