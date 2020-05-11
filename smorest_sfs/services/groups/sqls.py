#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Tuple

from sqlalchemy import literal_column, select
from sqlalchemy.sql import Join

from smorest_sfs.extensions import db
from smorest_sfs.modules.groups.models import groups_roles
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import Group, User, groups_users, roles_users
from smorest_sfs.plugins.sa import SAStatement


class DeleteGroupFromUser(SAStatement):
    def __init__(self, user: User, groups: List[Group]):
        # pylint: disable=W0231
        self._groups = groups
        self._group_ids = [g.id for g in self._groups]
        self._user = user
        self._build_sql()

    def _build_sql(self) -> None:
        user_role = db.alias(self._get_user_role_sql(), "user_role")
        self.sa_sql = roles_users.delete().where(
            db.and_(
                roles_users.c.role_id == user_role.c.role_id,
                roles_users.c.user_id == user_role.c.user_id,
            )
        )

    def __get_group_user_role_sql(self) -> select:
        return db.alias(
            db.select(
                [
                    groups_roles.c.group_id,
                    groups_users.c.user_id,
                    groups_roles.c.role_id,
                ]
            )
            .select_from(
                db.join(
                    groups_roles,
                    groups_users,
                    groups_users.c.group_id == groups_roles.c.group_id,
                )
            )
            .where(groups_users.c.user_id == self._user.id),
            "group_user_role",
        )

    def __get_role_sql_tuple(self) -> Tuple[select, select, Join]:
        group_user_role = self.__get_group_user_role_sql()
        remaining_role_sql = db.alias(
            db.select([group_user_role.c.role_id]).where(
                group_user_role.c.group_id.notin_(self._group_ids)
            ),
            "remaining_role_sql",
        )
        deleted_role_sql = db.alias(
            db.select([group_user_role.c.role_id]).where(
                group_user_role.c.group_id.in_(self._group_ids)
            ),
            "deleted_role_sql",
        )
        joined_role_sql = deleted_role_sql.outerjoin(
            remaining_role_sql,
            remaining_role_sql.c.role_id == deleted_role_sql.c.role_id,
        )
        return (remaining_role_sql, deleted_role_sql, joined_role_sql)

    def _get_user_role_sql(self) -> select:
        (
            remaining_role_sql,
            deleted_role_sql,
            joined_role_sql,
        ) = self.__get_role_sql_tuple()
        return (
            db.select(
                [
                    deleted_role_sql.c.role_id,
                    remaining_role_sql.c.role_id.label("r_role_id"),
                    literal_column(str(self._user.id), db.Integer).label("user_id"),
                ]
            )
            .select_from(joined_role_sql)
            .where(remaining_role_sql.c.role_id.is_(None))
        )


class AddUserToGroup(SAStatement):
    def __init__(self, user: User, groups: List[Group]):
        # pylint: disable=W0231
        self._groups = groups
        self._user = user
        self._build_sql()

    def _build_sql(self) -> None:
        absent_user_roles = self._get_absent_user_roles()
        self.sa_sql = roles_users.insert().from_select(
            ["user_id", "role_id"], absent_user_roles
        )

    def _get_absent_user_roles(self) -> select:
        roles_user = db.alias(
            db.select([roles_users]).where(roles_users.c.user_id == self._user.id),
            "roles_user",
        )
        joined_groups_user = db.outerjoin(
            groups_roles, roles_user, groups_roles.c.role_id == roles_user.c.role_id
        )
        return (
            db.select(
                [
                    db.func.coalesce(roles_user.c.user_id, self._user.id).label(
                        "user_id"
                    ),
                    groups_roles.c.role_id,
                ]
            )
            .select_from(joined_groups_user)
            .where(
                db.and_(
                    groups_roles.c.group_id.in_([g.id for g in self._groups]),
                    roles_user.c.role_id.is_(None),
                )
            )
            .distinct()
        )


class AddRoleToGroup(SAStatement):
    def __init__(self, group: Group, roles: List[Role]):
        # pylint: disable=W0231
        self._group = group
        self._roles = roles
        self._build_sql()

    def _build_sql(self) -> None:
        db.session.flush()
        self.__build_sql()

    def __build_sql(self) -> None:
        absent_users_roles = self._get_absent_users_roles()
        self.sa_sql = roles_users.insert().from_select(
            ["user_id", "role_id"], absent_users_roles
        )

    def _get_absent_users_roles(self) -> select:
        _users_roles = self._get_users_roles_sql()
        return (
            db.select([_users_roles.c.user_id, _users_roles.c.role_id])
            .select_from(
                db.outerjoin(
                    _users_roles,
                    roles_users,
                    db.and_(
                        _users_roles.c.role_id == roles_users.c.role_id,
                        _users_roles.c.user_id == roles_users.c.user_id,
                    ),
                )
            )
            .where(roles_users.c.user_id.is_(None))
        )

    def _get_users_roles_sql(self) -> select:
        group_users = db.alias(
            db.select([groups_users.c.user_id]).where(
                groups_users.c.group_id == self._group.id
            ),
            "group_users",
        )
        group_users_roles = db.join(
            group_users, groups_users, group_users.c.user_id == groups_users.c.user_id,
        ).join(groups_roles, groups_roles.c.group_id == groups_users.c.group_id)
        return db.alias(
            db.select([group_users.c.user_id, groups_roles.c.role_id,])
            .select_from(group_users_roles)
            .distinct(),
            "_users_roles",
        )


class DeleteRoleFromGroup(SAStatement):
    def __init__(self, group: Group, roles: List[Role]):
        # pylint: disable=W0231
        self._group = group
        self._roles = roles
        self._build_sql()

    def _build_sql(self) -> None:
        delete_users_roles_sql = db.alias(
            self._get_delete_users_roles(), "delete_users_roles"
        )
        self.sa_sql = roles_users.delete().where(
            db.and_(
                roles_users.c.role_id == delete_users_roles_sql.c.role_id,
                roles_users.c.user_id == delete_users_roles_sql.c.user_id,
            )
        )

    def _get_delete_users_roles(self) -> select:
        remain_users_roles, deleted_users_roles = self._get_absent_users_roles()
        return (
            db.select([deleted_users_roles.c.role_id, deleted_users_roles.c.user_id])
            .select_from(
                deleted_users_roles.outerjoin(
                    remain_users_roles,
                    db.and_(
                        remain_users_roles.c.role_id == deleted_users_roles.c.role_id,
                        remain_users_roles.c.user_id == deleted_users_roles.c.user_id,
                    ),
                )
            )
            .where(remain_users_roles.c.role_id.is_(None))
        )

    def _get_absent_users_roles(self) -> Tuple[select, select]:
        _users_group_roles = self._get_users_group_roles_sql()
        remaining_users_roles_sql = db.alias(
            db.select(
                [_users_group_roles.c.user_id, _users_group_roles.c.role_id]
            ).where(
                db.or_(
                    _users_group_roles.c.group_id != self._group.id,
                    _users_group_roles.c.role_id.notin_([r.id for r in self._roles]),
                )
            ),
            "reamaining_role_sql",
        )
        deleted_users_roles_sql = db.alias(
            db.select(
                [_users_group_roles.c.user_id, _users_group_roles.c.role_id]
            ).where(
                db.and_(
                    _users_group_roles.c.group_id == self._group.id,
                    _users_group_roles.c.role_id.in_([r.id for r in self._roles]),
                )
            ),
            "deleted_users_roles_sql",
        )
        return (remaining_users_roles_sql, deleted_users_roles_sql)

    def _get_users_group_roles_sql(self) -> select:
        group_users = db.alias(
            db.select([groups_users.c.user_id]).where(
                groups_users.c.group_id == self._group.id
            ),
            "group_users",
        )
        group_users_roles = db.join(
            group_users, groups_users, group_users.c.user_id == groups_users.c.user_id,
        ).join(groups_roles, groups_roles.c.group_id == groups_users.c.group_id)
        return db.alias(
            db.select(
                [group_users.c.user_id, groups_users.c.group_id, groups_roles.c.role_id]
            ).select_from(group_users_roles),
            "_users_roles",
        )


class AddMultiUserToGroup(AddRoleToGroup):
    def __init__(self, group: Group, users: List[User]):
        self._users = users
        super().__init__(group=group, roles=group.roles)

    def _build_sql(self) -> None:
        db.session.flush()
        self.__build_sql()

    def __build_sql(self) -> None:
        absent_users_roles = db.alias(
            self._get_absent_users_roles(), "absent_users_roles"
        )
        self.sa_sql = roles_users.insert().from_select(
            ["user_id", "role_id"],
            db.select([absent_users_roles]).where(
                absent_users_roles.c.user_id.in_([u.id for u in self._users])
            ),
        )


class DeleteMultiUserFromGroup(DeleteRoleFromGroup):
    def __init__(self, group: Group, users: List[User]):
        self._users = users
        super().__init__(group=group, roles=group.roles)

    def _build_sql(self) -> None:
        delete_users_roles_sql = db.alias(
            self._get_delete_users_roles(), "delete_users_roles"
        )
        target_delete_users_roles = db.alias(
            db.select([delete_users_roles_sql]).where(
                delete_users_roles_sql.c.user_id.in_([u.id for u in self._users])
            ),
            "target_delete_users_roles",
        )
        self._debug = db.select([delete_users_roles_sql])
        self.sa_sql = roles_users.delete().where(
            db.and_(
                roles_users.c.role_id == target_delete_users_roles.c.role_id,
                roles_users.c.user_id == target_delete_users_roles.c.user_id,
            )
        )
