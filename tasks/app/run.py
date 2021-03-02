# encoding: utf-8
# pylint: disable=too-many-arguments
"""
运行程序相关的Invoke模块
"""

import logging

from invoke import task

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@task(
    default=True,
    help={
        "debug": "是否加载Debug（默认：否）",
        "gunicorn": "是否从gunicorn启动（默认：否）",
        "bind": "bind地址（默认：127.0.0.1:5000）",
    },
)
def server(
    context, bind="127.0.0.1:5000", debug=True, gunicorn=False,
):
    """
    启动服务器
    """
    if gunicorn:
        command = f"gunicorn -b {bind} -k egg:meinheld#gunicorn_worker -c gunicorn.py smorest_sfs.app:app"
        context.run(command, pty=True)
    else:
        host, port = bind.split(":")
        from smorest_sfs.app import app

        app.run(host=host, port=port, debug=debug, use_reloader=debug)
