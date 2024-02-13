from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer,UserInfoSerializer

class UserView(viewsets.ModelViewSet):
    """
    用户信息的视图集，包括列表查询、创建、更新、删除等操作。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["list", "delete"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action == "update":
            return self.queryset.filter(id=self.request.user.id)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserInfoSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get"], url_path="self")
    def get_user_info(self, request, *args, **kwargs):
        """
        获取自己信息
        """
        instance = User.objects.get(id=self.request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

