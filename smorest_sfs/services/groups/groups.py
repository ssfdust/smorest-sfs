#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from loguru import logger

from smorest_sfs.extensions import db
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import Group, User
from smorest_sfs.plugins.sa import execute
from smorest_sfs.utils.sqla import get_histroy

from .sqls import AddRoleToGroup, DeleteRoleFromGroup, AddMultiUserToGroup, DeleteMultiUserFromGroup


def add_roles_to_group(group: Group, roles: List[Role]) -> None:
    if roles:
        logger.info(f"为组{group.name}添加{', '.join([r.name for r in roles])}角色")
        execute(AddRoleToGroup, group=group, roles=roles)


def delete_roles_from_group(group: Group, roles: List[Role]) -> None:
    if roles:
        logger.info(f"为组{group.name}删除{', '.join([r.name for r in roles])}角色")
        execute(DeleteRoleFromGroup, group=group, roles=roles)


def parse_group_change(group: Group) -> None:
    try:
        with db.session.no_autoflush:
            hist = get_histroy(group, "roles")
            delete_roles_from_group(group, hist.deleted)
            add_roles_to_group(group, hist.added)
    except ValueError:
        logger.debug(f"There is no changes in roles of group {group.name}")


def add_users_to_group(group: Group, users: List[User]) -> None:
    if users:
        logger.info(f"为组{group.name}添加{', '.join([u.nickname for u in users])}用户")
        execute(AddMultiUserToGroup, group=group, users=users)


def delete_users_from_group(group: Group, users: List[User]) -> None:
    if users:
        logger.info(f"为组{group.name}删除{', '.join([u.nickname for u in users])}用户")
        execute(DeleteMultiUserFromGroup, group=group, users=users)


def parse_group_users_change(group: Group) -> None:
    try:
        with db.session.no_autoflush:
            hist = get_histroy(group, "users")
            delete_users_from_group(group, hist.deleted)
            add_users_to_group(group, hist.added)
    except ValueError:
        logger.debug(f"There is no changes in users of group {group.name}")
