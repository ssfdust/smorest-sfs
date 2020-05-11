"""
数据初始化模板
"""
from datetime import datetime
from getpass import getpass
from typing import Any, List, Optional, Type

from smorest_sfs.extensions import db
from smorest_sfs.modules.auth.permissions import (
    DEFAULT_ROLES_PERMISSIONS_MAPPING as mapping,
)
from smorest_sfs.modules.auth.permissions import PERMISSIONS, ROLES
from smorest_sfs.modules.email_templates.models import EmailTemplate
from smorest_sfs.modules.roles.models import Permission, Role
from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.modules.users.models import Model, User, UserInfo
from smorest_sfs.modules.groups.models import Group
from smorest_sfs.utils.storages import load_avator_from_path


def create_item_from_cls(model_cls: Type[Model], cls: object) -> None:
    """根据类属性创建ORM"""
    names = [getattr(cls, attr) for attr in dir(cls) if not attr.startswith("__")]
    for name in names:
        model_cls(name=name).save()
    db.session.commit()


def _handle_default_role(role: Role) -> None:
    """hard code默认用户"""
    if role.name == ROLES.User:
        role.user_default = True


def init_permission() -> None:
    """根卷ROLES以及PERMISSION初始化权限"""
    create_item_from_cls(Role, ROLES)
    create_item_from_cls(Permission, PERMISSIONS)
    for role, permissions in mapping.items():
        permission_instances = Permission.where(name__in=permissions).all()
        role_instance = Role.where(name=role).first()
        _handle_default_role(role_instance)
        role_instance.permissions = permission_instances
        db.session.add(role_instance)
    db.session.commit()


def init_development_users(password: Optional[str] = None) -> None:
    """
    初始化数据
    """
    su_role = Role.get_by_name(name="SuperUser")
    if not password:
        password = getpass("Password:")

    # create super user
    root = User.create(
        username="wisdom",
        password=password,
        email="wisdom@zero.any.else",
        phonenum="1234567",
        active=True,
        confirmed_at=datetime.utcnow(),
    )
    avator = Storages(
        name="AdminAvator.jpg",
        storetype="avator",
        saved=True,
        filetype="image/jpeg",
        path="default/AdminAvator.jpg",
        uid=1,
        store=load_avator_from_path("default/AdminAvator.jpg"),
    )
    UserInfo.create(user=root, avator=avator)
    root.roles.append(su_role)
    root.save()


def get_or_create(model_cls: Type[Model], name: str) -> Any:
    """获取ORM或者根据name创建ORM

    只支持name字段的创建
    """
    item = model_cls.where(name=name).first()
    if item:
        return item
    return model_cls(name=name).save(False)


def get_or_create_from_lst(model_cls: Type[Model], *names: str) -> List[Any]:
    """根据一系列name字段获取ORM或者根据name创建ORM

    只支持name字段的获取与创建
    """
    lst = []
    for name in names:
        lst.append(get_or_create(model_cls, name))

    return lst


def update_permissions() -> None:
    """
    更新权限角色数据
    """
    for role_name, permissions in mapping.items():
        role = get_or_create(Role, role_name)
        permissions = get_or_create_from_lst(Permission, *permissions)
        role.add_permissions(permissions)

    db.session.commit()


def init_email_templates() -> None:
    """初始化邮件模板"""

    template = '<p>{{ message | safe }}</p><a href="{{ url }}" target="_blank">点击访问</a>'
    for name in ["default", "confirm", "reset-password"]:
        EmailTemplate.create(name=name, template=template)


def init_groups() -> None:
    """初始化用户组"""
    role = Role.get_by_name(ROLES.User)
    Group.create(name="默认用户组", description="默认用户组", default=True, roles=[role])
