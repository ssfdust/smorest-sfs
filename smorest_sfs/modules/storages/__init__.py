"""
    smorest_sfs.modules.storages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    文件系统模块

    用以管理系统的文件系统，负责文件的跟踪、
    上传与下载。
"""

from flask_smorest import Blueprint

blp = Blueprint("Storages", __name__, url_prefix="/storages", description="文件管理模块")
