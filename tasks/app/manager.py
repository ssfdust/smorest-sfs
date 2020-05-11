# encoding: utf-8
# pylint: disable=too-many-arguments
"""
supervisord相关的Invoke模块
"""

import logging
from pathlib import Path

from invoke import task

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@task
def status(context, config=".supervisord.conf"):
    """
    查询运行状态
    """
    command = f"supervisorctl -c {config} status"
    context.run(command)


@task(help={"program": "supervisord.conf中定义的program名"})
def start(context, program, config=".supervisord.conf"):
    """
    运行服务
    """
    command = f"supervisorctl -c {config} start {program}"
    context.run(command)


@task(help={"program": "supervisord.conf中定义的program名"})
def stop(context, program, config=".supervisord.conf"):
    """
    停止服务
    """
    command = f"supervisorctl  -c {config} stop {program}"
    context.run(command)


@task(help={"program": "supervisord.conf中定义的program名"})
def restart(context, program, config=".supervisord.conf"):
    """
    重启服务
    """
    command = f"supervisorctl -c {config} restart {program}"
    context.run(command)


@task(help={"program": "supervisord.conf中定义的program名"})
def logs(context, program="gunicorn", config=".supervisord.conf"):
    """
    打印Supervord日志
    默认: gunicorn
    """
    command = f"supervisorctl -c {config} fg {program}"
    context.run(command)


@task
def shutdown(context, config=".supervisord.conf"):
    """
    关闭supervord
    """
    command = f"supervisorctl -c {config} shutdown"
    context.run(command)


@task(default=True)
def daemon(context, config=".supervisord.conf"):
    """
    从supervord启动多服务.
    """

    log_path = Path("logs")
    if not log_path.exists():
        log_path.mkdir()
    command = f"supervisord -c {config}"
    context.run(command)
