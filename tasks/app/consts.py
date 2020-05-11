#!/usr/bin/env python
# -*- coding: utf-8 -*-


BACKUP_PERMISSIONS_FILE = "smorest_sfs/modules/auth/permissions.bak.py"
NEW_PERMISSIONS_FILE = "smorest_sfs/modules/auth/permissions.new.py"
PERMISSIONS_FILE = "smorest_sfs/modules/auth/permissions.py"

CONFIG_PATH = "config/{config}.toml"
NGINX_PATH = "deploy/nginx/flask.conf"
MONGO_PATH = "cmds/{config}_mongodb.txt"
SQL_PATH = "cmds/{config}_create.sql"
SQLSH_PATH = "cmds/{config}_createpg.sh"

CONFIG_TYPES = ["development", "production", "testing"]

EOF_ROLES = "# End Of ROLES"
EOF_PEMISSIONS = "# End Of PERMISSIONS"
EOF_SU = "# End Of SuperUser"
EOF_MAPPING = "# End Of Permissions Mapping"

ADDED_ROLE = "{model_name}Manager = '{model_name}Manager'\n" f"    {EOF_ROLES}"
ADDED_PERMISSIONS = (
    "# {model_name}Manager\n"
    "    {model_name}Add = '{model_name}AddPrivilege'\n"
    "    {model_name}Edit = '{model_name}EditPrivilege'\n"
    "    {model_name}Delete = '{model_name}DeletePrivilege'\n"
    "    {model_name}Query = '{model_name}QueryPrivilege'\n"
    f"    {EOF_PEMISSIONS}"
)
ADDED_SU = (
    "# {module_title}管理\n"
    "        PERMISSIONS.{model_name}Add, PERMISSIONS.{model_name}Delete,\n"
    "        PERMISSIONS.{model_name}Edit, PERMISSIONS.{model_name}Query,\n"
    f"        {EOF_SU}"
)
ADDED_MAPPING = (
    "ROLES.{model_name}Manager: [\n"
    "        PERMISSIONS.{model_name}Add, PERMISSIONS.{model_name}Delete,\n"
    "        PERMISSIONS.{model_name}Edit, PERMISSIONS.{model_name}Query\n"
    "    ],\n"
    f"    {EOF_MAPPING}"
)
