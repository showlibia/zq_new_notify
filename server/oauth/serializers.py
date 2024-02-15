from datetime import datetime
from typing import Any, Dict

from rest_framework_simplejwt.serializers import PasswordField
from users.models import User
from wechat.wxa import get_openid
from zq_django_util.utils.auth.backends import OpenIdBackend
from zq_django_util.utils.auth.serializers import (
    OpenIdLoginSerializer as DefaultOpenIdLoginSerializer,
)

def generate_token_result(
    user: User,
    user_id_field: str,
    expire_time: datetime,
    access: str,
    refresh: str,
) -> dict:
    return dict(
        id=getattr(user, user_id_field),
        username=user.username,
        is_authenticated=user.is_authenticated,
        is_staff=user.is_staff,
        expire_time=expire_time,
        access=access,
        refresh=refresh,
    )

class OpenIdLoginSerializer(DefaultOpenIdLoginSerializer):
    """
    OpenID Token 获取序列化器 (直接用 openid 获取登录 token，用于测试)
    """

    backend = OpenIdBackend(User)  # 自定义验证后端，用于指定不同类型的用户模型

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_token_result(
        self,
        user: User,
        user_id_field: str,
        expire_time: datetime,
        access: str,
        refresh: str,
    ) -> dict:
        return generate_token_result(
            user, user_id_field, expire_time, access, refresh
        )


class WechatLoginSerializer(OpenIdLoginSerializer):
    """
    微信登录序列化器
    """

    code = PasswordField(label="前端获取code")  # 前端传入 code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop("openid")  # 删除 openid 字段

    def get_open_id(self, attrs: Dict[str, Any]) -> str:
        """
        重写获取 open_id 方法
        """
        return get_openid(attrs["code"])
