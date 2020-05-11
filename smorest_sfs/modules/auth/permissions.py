#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    权限定义以及映射模块，此模块用以建立默认的
    角色权限关系，修改后通过
    `inv app.db.update-app-permissions`
    进行更新权限关系
"""


class ROLES:
    """角色字段定义"""

    SuperUser = "SuperUser"
    User = "User"
    UserManager = "UserManager"
    EmailTemplateManager = "EmailTemplateManager"
    RoleManager = "RoleManager"
    GroupManager = "GroupManager"
    ProjectManager = "ProjectManager"
    CodeManager = "CodeManager"
    MenuManager = "MenuManager"
    LogManager = "LogManager"
    groupManager = "groupManager"
    # End Of ROLES


class PERMISSIONS:
    """权限字段定义"""

    SuperUser = "SuperUserPrivilege"
    User = "UserPrivilege"
    # RoleManager
    RoleAdd = "RoleAddPrivilege"
    RoleDelete = "RoleDeletePrivilege"
    RoleEdit = "RoleEditPrivilege"
    RoleQuery = "RoleQueryPrivilege"
    # UserManager
    UserAdd = "UserAddPrivilege"
    UserDelete = "UserDeletePrivilege"
    UserEdit = "UserEditPrivilege"
    UserQuery = "UserQueryPrivilege"
    # GroupManager
    GroupAdd = "GroupAddPrivilege"
    GroupDelete = "GroupDeletePrivilege"
    GroupEdit = "GroupEditPrivilege"
    GroupQuery = "GroupQueryPrivilege"
    # EmailTemplateManager
    EmailTemplateAdd = "EmailTemplateAddPrivilege"
    EmailTemplateEdit = "EmailTemplateEditPrivilege"
    EmailTemplateDelete = "EmailTemplateDeletePrivilege"
    EmailTemplateQuery = "EmailTemplateQueryPrivilege"
    # FileManager
    FileForceDelete = "FileForceDeletePrivilege"
    # ProjectManager
    ProjectAdd = "ProjectAddPrivilege"
    ProjectEdit = "ProjectEditPrivilege"
    ProjectDelete = "ProjectDeletePrivilege"
    ProjectQuery = "ProjectQueryPrivilege"
    # CodeManager
    CodeAdd = "CodeAddPrivilege"
    CodeEdit = "CodeEditPrivilege"
    CodeDelete = "CodeDeletePrivilege"
    CodeQuery = "CodeQueryPrivilege"
    # MenuManager
    MenuAdd = "MenuAddPrivilege"
    MenuEdit = "MenuEditPrivilege"
    MenuDelete = "MenuDeletePrivilege"
    MenuQuery = "MenuQueryPrivilege"
    # LogManager
    LogAdd = "LogAddPrivilege"
    LogEdit = "LogEditPrivilege"
    LogDelete = "LogDeletePrivilege"
    LogQuery = "LogQueryPrivilege"
    # groupManager
    groupAdd = "groupAddPrivilege"
    groupEdit = "groupEditPrivilege"
    groupDelete = "groupDeletePrivilege"
    groupQuery = "groupQueryPrivilege"
    # End Of PERMISSIONS


# 默认的角色权限映射

DEFAULT_ROLES_PERMISSIONS_MAPPING = {
    ROLES.User: [PERMISSIONS.User],
    ROLES.SuperUser: [
        PERMISSIONS.SuperUser,
        PERMISSIONS.User,
        # 用户管理
        PERMISSIONS.UserAdd,
        PERMISSIONS.UserDelete,
        PERMISSIONS.UserEdit,
        PERMISSIONS.UserQuery,
        # 用户组管理
        PERMISSIONS.GroupAdd,
        PERMISSIONS.GroupDelete,
        PERMISSIONS.GroupEdit,
        PERMISSIONS.GroupQuery,
        PERMISSIONS.UserEdit,
        # 用户角色管理
        PERMISSIONS.RoleAdd,
        PERMISSIONS.RoleDelete,
        PERMISSIONS.RoleEdit,
        PERMISSIONS.RoleQuery,
        # 电子邮件模板管理
        PERMISSIONS.EmailTemplateAdd,
        PERMISSIONS.EmailTemplateDelete,
        PERMISSIONS.EmailTemplateEdit,
        PERMISSIONS.EmailTemplateQuery,
        PERMISSIONS.FileForceDelete,
        # 项目管理
        PERMISSIONS.ProjectAdd,
        PERMISSIONS.ProjectDelete,
        PERMISSIONS.ProjectEdit,
        PERMISSIONS.ProjectQuery,
        # 编码管理
        PERMISSIONS.CodeAdd,
        PERMISSIONS.CodeDelete,
        PERMISSIONS.CodeEdit,
        PERMISSIONS.CodeQuery,
        # 菜单管理
        PERMISSIONS.MenuAdd,
        PERMISSIONS.MenuDelete,
        PERMISSIONS.MenuEdit,
        PERMISSIONS.MenuQuery,
        # 日志管理
        PERMISSIONS.LogAdd,
        PERMISSIONS.LogDelete,
        PERMISSIONS.LogEdit,
        PERMISSIONS.LogQuery,
        # 用户组管理
        PERMISSIONS.groupAdd,
        PERMISSIONS.groupDelete,
        PERMISSIONS.groupEdit,
        PERMISSIONS.groupQuery,
        # End Of SuperUser
    ],
    ROLES.GroupManager: [
        PERMISSIONS.GroupAdd,
        PERMISSIONS.GroupDelete,
        PERMISSIONS.GroupEdit,
        PERMISSIONS.GroupQuery,
    ],
    ROLES.UserManager: [
        PERMISSIONS.UserAdd,
        PERMISSIONS.UserDelete,
        PERMISSIONS.UserEdit,
        PERMISSIONS.UserQuery,
    ],
    ROLES.RoleManager: [
        PERMISSIONS.RoleAdd,
        PERMISSIONS.RoleDelete,
        PERMISSIONS.RoleEdit,
        PERMISSIONS.RoleQuery,
    ],
    ROLES.EmailTemplateManager: [
        PERMISSIONS.EmailTemplateAdd,
        PERMISSIONS.EmailTemplateDelete,
        PERMISSIONS.EmailTemplateEdit,
        PERMISSIONS.EmailTemplateQuery,
    ],
    ROLES.ProjectManager: [
        PERMISSIONS.ProjectAdd,
        PERMISSIONS.ProjectDelete,
        PERMISSIONS.ProjectEdit,
        PERMISSIONS.ProjectQuery,
    ],
    ROLES.CodeManager: [
        PERMISSIONS.CodeAdd,
        PERMISSIONS.CodeDelete,
        PERMISSIONS.CodeEdit,
        PERMISSIONS.CodeQuery,
    ],
    ROLES.MenuManager: [
        PERMISSIONS.MenuAdd,
        PERMISSIONS.MenuDelete,
        PERMISSIONS.MenuEdit,
        PERMISSIONS.MenuQuery,
    ],
    ROLES.LogManager: [
        PERMISSIONS.LogAdd,
        PERMISSIONS.LogDelete,
        PERMISSIONS.LogEdit,
        PERMISSIONS.LogQuery,
    ],
    ROLES.groupManager: [
        PERMISSIONS.groupAdd,
        PERMISSIONS.groupDelete,
        PERMISSIONS.groupEdit,
        PERMISSIONS.groupQuery,
    ],
    # End Of Permissions Mapping
}
