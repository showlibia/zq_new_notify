from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from groups.serializers import NotificationSerializer, GroupSerializer
from users.models import User
from users.serializers import UserInfoSerializer, UserSerializer

from .models import Attendance, Notification, Group


class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(id=self.request.user.id)
        else:
            return super().get_queryset()

    def list(self, request, *args, **kwargs):
        """
        获取社团信息
        """
        queryset = self.get_queryset().first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def check_in(self, request):
        """
        签到
        """
        user_id = request.user.id  # 获取当前登录用户的id
        attendance = Attendance.objects.filter(user_id=user_id).first()
        if attendance:
            attendance.attendance = True
            attendance.save()
            return JsonResponse({"success": True, "message": "签到成功"}, status=status.HTTP_200_OK)  # 签到成功
        else:
            # 获取未签到人员名单
            absent_users = []
            all_users = User.objects.all()
            for user in all_users:
                if not Attendance.objects.filter(user_id=user.id, attendance=True).exists():
                    absent_users.append(user.username)

            return JsonResponse(
                {
                    "success": False,
                    "message": "未签到",
                    "absent_users": absent_users
                },
                status=status.HTTP_200_OK
            )

    def notice(self, request):
        """
        新增通知
        """
        publisher = request.user

        # 解析请求中的通知内容
        serializer = NotificationSerializer(data=request.data)

        # 如果请求数据无效，返回错误响应
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 创建通知对象并保存到数据库中
        notification = Notification(publisher=publisher, content=serializer.validated_data['content'])
        notification.save()

        # 返回成功响应
        return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)

    def edit_notice(self, notice_id):
        """
        修改通知
        """
        try:
            # 根据通知ID获取要修改的通知对象
            notification = Notification.objects.get(id=notice_id)
        except Notification.DoesNotExist:
            return Response({"error": "通知不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 解析请求中的通知内容
        serializer = NotificationSerializer(notification, data=self.data, partial=True)

        # 如果请求数据无效，返回错误响应
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 保存修改后的通知内容到数据库中
        serializer.save()

        # 返回成功响应
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
    def confirm_notification_received(self, request, notification_id):
        try:
            notification = Notification.objects.get(pk=notification_id)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            receiver = NotificationReceiver.objects.get(notification=notification, user=user)
        except NotificationReceiver.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)

        receiver.received = True
        receiver.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


# Create your views here.
