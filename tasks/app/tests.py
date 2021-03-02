# encoding: utf-8
# pylint: disable=invalid-name,unused-argument,too-many-arguments
"""
单元测试相关的Invoke模块
"""
import logging

from invoke import task

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@task(
    default=True,
    help={"directory": "单元测试目录", "cov": "开启覆盖率检测 （默认：否）"},
    incrementable=["verbose"],
)
def tests(context, directory="tests", cov=False, verbose=0):
    """
    对项目进行单元测试
    """
    import pytest

    command = [directory]
    if cov:
        cov_dir = directory.replace("tests", "smorest_sfs")
        command.extend(["--cov", cov_dir, "--cov-report", "term-missing"])
    if verbose:
        command.extend(["--pdb", "-" + "v" * verbose])
    if verbose >= 2:
        command.extend(["-s"])
    if verbose == 3:
        command.extend(["--full-trace"])
    return pytest.main(command)
