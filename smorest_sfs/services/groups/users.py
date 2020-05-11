#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from loguru import logger

from smorest_sfs.extensions import db
from smorest_sfs.modules.users.models import Group, User
from smorest_sfs.plugins.sa import execute
from smorest_sfs.utils.sqla import get_histroy

from .sqls import AddUserToGroup, DeleteGroupFromUser


def add_groups_roles_to_user(user: User, groups: List[Group]) -> None:
    if groups:
        logger.info(f"为用户{user.nickname}添加{', '.join([g.name for g in groups])}组的角色")
        execute(AddUserToGroup, user=user, groups=groups)


def delete_groups_roles_from_user(user: User, groups: List[Group]) -> None:
    if groups:
        logger.info(f"为用户{user.nickname}删除{', '.join([g.name for g in groups])}组的角色")
        execute(DeleteGroupFromUser, user=user, groups=groups)


def set_default_groups_for_user(user: User) -> User:
    groups = Group.query.filter_by(default=True).all()
    non_related_groups = [group for group in groups if group not in user.groups]
    if non_related_groups:
        user.groups.extend(non_related_groups)
        add_groups_roles_to_user(user, groups)
    return user


def parse_user_groups_change(user: User) -> None:
    try:
        with db.session.no_autoflush:
            hist = get_histroy(user, "groups")
            delete_groups_roles_from_user(user, hist.deleted)
            add_groups_roles_to_user(user, hist.added)
    except ValueError:
        logger.debug(f"There is no changes in groups of user {user.nickname}")
