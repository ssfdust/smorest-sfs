"""Initilize the database and prepare the data

Revision ID: 00000001
Revises: None
Create Date: 2020-04-23 19:48:48.084856

"""
from migrations import initial_data
from smorest_sfs.extensions import db

# revision identifiers, used by Alembic.
revision = '00000001'
down_revision = None


def upgrade() -> None:
    from smorest_sfs.services.users import create_user
    from smorest_sfs.modules.users.schemas import UserRegisterSchema
    db.create_all()
    initial_data.init_permission()
    data = {
        "phonenum": "18718188181",
        "username": "kanno",
        "confirmed_at": "2020-04-30 00:00:00",
        "email": "kanno@mail.com",
        "password": "kanno",
        "active": True,
        "userinfo": {"first_name": "飘", "last_name": "尘", "sex": 1, "age": 26}
    }
    user = UserRegisterSchema().load(data)
    create_user(user, is_admin=True)
    initial_data.init_email_templates()


def downgrade() -> None:
    db.drop_all()
