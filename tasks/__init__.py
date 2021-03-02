# encoding: utf-8
# pylint: disable=invalid-name,wrong-import-position
"""
本项目Invoke Task的入口

基本上是frol/flask-restplus-server-example的一个翻版，
很多都是沿用的frol的配置，然后做了优化与汉化。
出处：https://github.com/frol/flask-restplus-server-example
"""

import os
import platform

from invoke import Collection
from invoke.executor import Executor

from . import app, logger

# NOTE: `namespace` or `ns` name is required!
namespace = Collection(app,)


def invoke_execute(context, command_name, **kwargs):
    """
    执行Invoke Task的帮助函数
    """
    results = Executor(namespace, config=context.config).execute((command_name, kwargs))
    target_task = context.root_namespace[command_name]
    return results[target_task]


namespace.configure(
    {
        "run": {
            "shell": "/bin/sh"
            if platform.system() != "Windows"
            else os.environ.get("COMSPEC"),
        },
        "root_namespace": namespace,
        "invoke_execute": invoke_execute,
    }
)
