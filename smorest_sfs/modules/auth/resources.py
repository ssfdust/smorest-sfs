"""
    app.modules.auth
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    用户验证的API资源模块
"""
from datetime import datetime
from typing import Any, Dict, Optional, TypeVar, Union

from captcha.image import ImageCaptcha
from flask import current_app as app
from flask import send_file, url_for
from flask.views import MethodView
from flask_jwt_extended import create_access_token, current_user, get_jwt_identity
from flask_smorest import abort
from loguru import logger

from smorest_sfs.extensions.marshal import BaseMsgSchema
from smorest_sfs.extensions.storage.captcha import CaptchaStore
from smorest_sfs.modules.users.models import User
from smorest_sfs.services.auth.auth import UserLoginChecker, login_user, logout_user
from smorest_sfs.services.auth.confirm import (
    confirm_current_token,
    generate_confirm_token,
)
from smorest_sfs.services.mail import PasswdMailSender

from . import blp, params, schemas
from .decorators import doc_login_required, doc_refresh_required
from .helpers import add_token_to_database

Response = TypeVar("Response")


@blp.route("/login")
class LoginView(MethodView):
    @blp.arguments(params.LoginParams, location="json")
    @blp.response(schemas.UserViewPostSchema, description="登录成功")
    def post(
        self, args: Dict[str, str]
    ) -> Dict[str, Union[int, str, Dict[str, Dict[str, str]]]]:
        """
        用户登录

        用户名密码登录后，返回基本信息以及token，
        登录方式为token方式
        """
        with UserLoginChecker(
            args["email"], args["password"], args["captcha"], args["token"]
        ).check() as user:
            data = login_user(user)

        return {"code": 0, "msg": "success", "data": data}


@blp.route("/captcha")
class CaptchaView(MethodView):
    @blp.arguments(params.CaptchaParam, location="query", as_kwargs=True)
    @blp.response(description="图片")
    def get(self, token: str) -> Response:
        """
        获取验证码图片

        每次随机生成一个token来获取图片，延时时间为5分钟
        """
        image = ImageCaptcha()
        store = CaptchaStore(token)
        code = store.generate_captcha()
        data = image.generate(code)

        return send_file(data, attachment_filename="captcha.jpeg")


@blp.route("/forget-password")
class ForgetPasswordView(MethodView):
    @blp.arguments(params.EmailParam, as_kwargs=True)
    @blp.response(BaseMsgSchema, description="成功")
    def post(self, email: str) -> Optional[Dict[str, Union[str, int]]]:
        """
        忘记密码

        发送忘记密码邮件到请求的email
        """
        user = User.get_by_keyword(email)
        if not user:
            abort(404, message="用户不存在")
        logger.info(f"{user.email}发起了忘记密码申请")

        token = generate_confirm_token(user, "passwd")
        url = url_for("Auth.ResetForgotPasswordView", token=token, _external=True)
        if user.email:
            sender = PasswdMailSender(
                to=user.email, content={"url": url, "message": "找回密码"}
            )
            sender.send()
        else:
            abort(404, message="未填写电子邮箱")
        return {"code": 0, "msg": "success"}


@blp.route("/confirm")
class UserConfirmView(MethodView):
    @doc_login_required
    @blp.response(BaseMsgSchema, description="验证成功")
    def get(self) -> Dict[str, Union[str, int]]:
        """
        完成用户验证
        """
        user = confirm_current_token("confirm")

        user.update(confirmed_at=datetime.utcnow(), active=True)
        logger.info(f"{user.email}完成了用户验证")

        return {"code": 0, "msg": "success"}


@blp.route("/reset-forgot-password")
class ResetForgotPasswordView(MethodView):
    @doc_login_required
    @blp.arguments(params.PasswdParam, as_kwargs=True)
    @blp.response(BaseMsgSchema, description="验证成功")
    def put(self, password: str, confirm_password: str) -> Dict[str, Union[int, str]]:
        """
        忘记密码后修改

        根据token设置密码
        """

        if password != confirm_password:
            abort(501, message="密码不一致，修改失败")

        user = confirm_current_token("passwd")
        logger.info(f"{user.email} 修改了密码")
        user.update(password=confirm_password)

        return {"code": 0, "msg": "success"}

    @doc_login_required
    @blp.response(BaseMsgSchema, description="可以访问")
    def get(self) -> Dict[str, Any]:
        """
        忘记密码token测试

        测试token是否可用
        """
        confirm_current_token("passwd", revoked=False)

        return {"code": 0, "msg": "success"}


@blp.route("/refresh")
class RefreshJwtTokenView(MethodView):
    @doc_refresh_required
    @blp.response(schemas.RefreshViewPostSchema, description="获取成功")
    def post(self) -> Dict[str, Any]:
        """
        用户刷新Token

        用户用refresh_token获取新的token
        """
        user_identity = get_jwt_identity()
        access_token = create_access_token(identity=user_identity)
        add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
        logger.info(f"{current_user} 刷新了token")

        return {"code": 0, "msg": "success", "data": {"access_token": access_token}}


@blp.route("/logout")
class LogoutView(MethodView):
    @doc_login_required
    @blp.response(BaseMsgSchema, description="登出成功")
    def post(self) -> Dict[str, Union[str, int]]:
        """
        用户登出

        带着token并以refresh_token为参数访问此api，即可完成登出，token失效
        """
        logout_user(current_user)

        return {"code": 0, "msg": "success"}
