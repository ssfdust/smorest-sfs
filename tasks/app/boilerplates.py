# pylint: disable=line-too-long
"""
模板相关的Invoke模块
"""
import logging
import os
import shutil

from invoke import task

from tasks.app._utils import create_dirs
from tasks.app.consts import (
    ADDED_MAPPING,
    ADDED_PERMISSIONS,
    ADDED_ROLE,
    ADDED_SU,
    BACKUP_PERMISSIONS_FILE,
    EOF_MAPPING,
    EOF_PEMISSIONS,
    EOF_ROLES,
    EOF_SU,
    NEW_PERMISSIONS_FILE,
    PERMISSIONS_FILE,
)
from tasks.app.crud import CrudOpts

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@task
def generate_config(context):
    # pylint: disable=unused-argument
    """
    新建配置内容，根据提示新建配置

    用法:
    $ invoke app.boilerplates.generate_config
    """
    from tasks.app.config import Config
    from tasks.app.renders import render_config_to_toml

    create_dirs()

    # Genrate configuration
    configs = Config()
    configs.set_configurations()

    render_config_to_toml(configs)

    log.info("配置文件生成完毕.")


@task(
    help={
        "module_name": "模块名称",
        "module_title": "模块标题（注释用）",
        "module_name_singular": "模块单例名",
        "description": "模块描述",
    }
)
def crud_module(context, module_name="", module_name_singular="", module_title=""):
    # pylint: disable=unused-argument
    """
    新建一个增删改查模块
    来源：frol/flask-restplus-server-example

    用法:
    $ inv app.boilerplates.crud-module --module-name=articles \
                --module-name-singular=article \
                --module_title=文章

    """
    from tasks.app.renders import render_crud_modules

    opts = CrudOpts(module_name, module_name_singular, module_title)

    render_crud_modules(module_name, opts.to_config())

    # permissions_adder(context, model_name=config["model_name"],
    # module_title=config["module_title"])

    log.info("模块 `%s` 创建成功.", module_name)

    log.info("请在app/factory.py中的ENABLED_MODULES中添加新模块以激活。")


@task
def apply_changes(context):
    # pylint: disable=unused-argument
    """
    应用新模块的权限
    """

    if os.path.exists(BACKUP_PERMISSIONS_FILE):
        os.remove(BACKUP_PERMISSIONS_FILE)
    orders = [
        [PERMISSIONS_FILE, BACKUP_PERMISSIONS_FILE],
        [NEW_PERMISSIONS_FILE, PERMISSIONS_FILE],
    ]
    for orig, dst in orders:
        log.info("移动%s到%s", orig, dst)
        shutil.move(orig, dst)
    log.info("应用完毕")


@task(help={"model_name": "模块ORM名", "module_title": "模块名"})
def permissions_adder(context, model_name="", module_title=""):
    # pylint: disable=unused-argument
    """
    为权限文件新增新的模块权限

    用法:
    $ inv app.boilerplates.permissions-adder --module-name=articles \
                --module_title=文章

    """

    added_role = ADDED_ROLE.format(model_name=model_name)
    added_permissions = ADDED_PERMISSIONS.format(model_name=model_name)
    added_su = ADDED_SU.format(model_name=model_name, module_title=module_title)
    added_mapping = ADDED_MAPPING.format(model_name=model_name)

    with open("smorest_sfs/modules/auth/permissions.py") as f:
        text = f.read()

    for orig, subs in [
        [EOF_ROLES, added_role],
        [EOF_PEMISSIONS, added_permissions],
        [EOF_SU, added_su],
        [EOF_MAPPING, added_mapping],
    ]:
        text = text.replace(orig, subs)

    with open("smorest_sfs/modules/auth/permissions.new.py", "w") as f:
        f.write(text)

    log.info("新权限文件 `%s` 生成成功.\n", "app/modules/auth/permissions.new.py")
    log.info("请编辑后替换旧权限文件，并执行`invoke app.db.update-app-permissions`")


@task
def generate_docker_compose(context):
    # pylint: disable=unused-argument
    from tasks.app.config import Config
    from tasks.app.renders import render_config_to_dockercompose

    configs = Config().load_configurations()
    render_config_to_dockercompose(configs)
