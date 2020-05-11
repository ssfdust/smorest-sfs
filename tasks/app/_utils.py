# encoding: utf-8
"""
Invoke中App相关工具
"""
import functools
import os
import platform
from pathlib import Path

from invoke import Task as BaseTask

from tasks.app.consts import CONFIG_PATH, NGINX_PATH, SQL_PATH

try:
    import readline
except ImportError:
    pass


class Task(BaseTask):
    """
    封装Task以便于支持装饰器
    """

    def argspec(self, body):
        """
        详情： https://github.com/pyinvoke/invoke/pull/399.
        """
        if hasattr(body, "__wrapped__"):
            return self.argspec(body.__wrapped__)
        return super(Task, self).argspec(body)


def app_context_task(*args, **kwargs):
    """
    Invoke中应用的app_context

    示例:

    >>> @app_context_task
    ... def my_task(context, some_arg, some_option='default'):
    ...     print("Done")

    >>> @app_context_task(
    ...     help={'some_arg': "This is something useful"}
    ... )
    ... def my_task(context, some_arg, some_option='default'):
    ...     print("Done")
    """
    if len(args) == 1:
        func = args[0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            A wrapped which tries to get ``app`` from ``kwargs`` or creates a
            new ``app`` otherwise, and actives the application context, so the
            decorated function is run inside the application context.
            """
            app = kwargs.pop("app", None)
            if app is None:
                from smorest_sfs.app import app

            with app.app_context():
                return func(*args, **kwargs)

        return Task(wrapper, **kwargs)

    return lambda func: app_context_task(func, **kwargs)


def rlinput(prompt, prefill=""):
    if platform.system() == "Windows":
        from .winpress import sendkeys

        sendkeys(prefill)
        return input(prompt)
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)  # or raw_input in Python 2
    finally:
        readline.set_startup_hook()


def create_dirs():
    for the_path in [CONFIG_PATH, NGINX_PATH, SQL_PATH]:
        configdir = Path(the_path).parent
        if not os.path.exists(configdir):
            configdir.mkdir(parents=True)
