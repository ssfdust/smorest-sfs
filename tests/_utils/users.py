from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from smorest_sfs.modules.users.models import User


def generate_user_instance(
    username: str = "username",
    phonenum: Optional[str] = None,
    is_active: bool = True,
    **kwargs: Any
) -> "User":
    """
    Returns:
        user_instance (User) - an not committed to DB instance of a User model.
    """
    from smorest_sfs.modules.users.models import User, UserInfo

    password = "%s_password" % username
    user_instance = User(
        id_=kwargs.get("user_id", None),
        phonenum=phonenum or "12345678",
        active=is_active,
        username=username,
        email="%s@email.com" % username,
        password=password,
        userinfo=UserInfo(sex=1, age=1),
    )
    return user_instance
