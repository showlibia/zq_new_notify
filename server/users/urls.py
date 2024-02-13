from rest_framework import routers
from .views import UserView

urlpatterns = []

router = routers.SimpleRouter()

router.register(r'', UserView, basename='user')
urlpatterns += router.urls # 拼接生成的路由