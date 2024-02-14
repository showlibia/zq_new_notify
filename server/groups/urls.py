from rest_framework import routers

from groups.views import GroupView

urlpatterns = []

router = routers.DefaultRouter()

router.register(r'', GroupView, basename='user')
urlpatterns += router.urls
