# encoding: utf-8
# pylint: disable=invalid-name,unused-argument,too-many-arguments
"""
单元测试相关的Invoke模块
"""
import logging

from invoke import task

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@task(
    default=True, help={"directory": "单元测试目录", "with-pdb": "开启pdb支持 （默认：否）",},
)
def tests(context, directory="tests", pdb=False, cov=True):
    """
    对项目进行单元测试
    """
    import pytest

    command = [directory]
    if pdb:
        command.extend(["--pdb", "-s", "-vvv", "--full-trace"])
    if cov:
        cov_dir = directory.replace("tests", "smorest_sfs")
        command.extend(["--cov", cov_dir, "--cov-report", "term-missing"])
    return pytest.main(command)
