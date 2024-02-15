from django.conf import settings
from django.core.cache import caches
from wechatpy.client import WeChatClient
from wechatpy.session import SessionStorage


class WechatCache(SessionStorage):
    def __init__(self, cache):
        self.cache = cache

    def get(self, key, default=None):
        return self.cache.get(key, default)

    def set(self, key, value, ttl=None):
        self.cache.set(key, value, timeout=ttl)

    def delete(self, key):
        self.cache.delete(key)

wechat_client = WeChatClient(
    settings.WECHAT_APPID,
    settings.WECHAT_APPSECRET,
    session=WechatCache(caches['default'])
)