# encoding: utf-8
"""
与用户相关的Invoke模块
"""
import getpass
from datetime import datetime

from tasks.app._utils import app_context_task

#  from app.extensions import bcrypt
#
#  pw_hash = bcrypt.generate_password_hash(self.password).decode('utf-8')


@app_context_task(
    help={"email": "用户邮箱", "is-admin": "是否admin（默认：是）", "is-active": "启用（默认：是）",}
)
def create_user(context, email, is_admin=True, is_active=True):
    # pylint: disable=unused-argument
    """
    新建用户
    """
    from smorest_sfs.services.users import create_user as _create_user
    from smorest_sfs.modules.users.models import User

    username = email.split("@")[0]
    password = getpass.getpass("Password:")
    user = User(
        username=username,
        email=email,
        password=password,
        active=is_active,
        confirmed_at=datetime.utcnow(),
    )
    _create_user(user, is_admin)
