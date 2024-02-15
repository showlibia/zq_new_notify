from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    OpenIdLoginView,
    WechatLoginView,
)

router = routers.SimpleRouter()

urlpatterns = [
    path("wechat/", WechatLoginView.as_view(), name="wechat_login"),  # 微信登录
    path(
        "refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # 刷新token
    path(
        "wechat/openid/", OpenIdLoginView.as_view(), name="openid_pair"
    ),  # openid登录
]

urlpatterns += router.urls