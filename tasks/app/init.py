# encoding: utf-8
# pylint: disable=invalid-name,unused-argument,too-many-arguments
"""
数据以及初始化相关的Invoke模块
"""
import logging

from invoke import task

from ._utils import app_context_task

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@app_context_task(help={"skip_on_failure": "忽略错误（默认：否）"})
def init_development_data(context, skip_on_failure=False, password=None):
    """
    初始化诸如用户、用户权限等基本信息到数据库
    """

    log.info("初始化应用数据...")

    from migrations import initial_data

    try:
        initial_data.init_permission()
        initial_data.init_development_users(password)
        initial_data.init_email_templates()
        initial_data.update_permissions()
    except AssertionError as exception:
        if not skip_on_failure:
            log.error("%s", exception)
        else:
            log.info("Initializing development data step is skipped.")
    else:
        log.info("数据初始化成功.")


@app_context_task
def update_app_permissions(context):
    """
    更新权限
    """

    log.info("正在更新应用权限...")
    from migrations import initial_data

    initial_data.update_permissions()

    log.info("应用权限更新完毕.")


@app_context_task
def dropdb(context):
    """
    删除数据库
    """
    from smorest_sfs.extensions import db

    db.drop_all()


@app_context_task
def initdb(context):
    """
    初始化数据库
    """
    from smorest_sfs.extensions import db

    db.create_all()
