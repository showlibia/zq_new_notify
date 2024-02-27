from rest_framework import serializers
from users.models import User
from users.serializers import UserInfoSerializer, UserTeamMemberSerializer
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType

from .models import Group, GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = [
            "id",
            "user",
        ]

    def create(self, validated_data):
        return GroupMember.objects.create(
            **validated_data,
            group=self.context["request"].group,
        )

    def validate_user(self, value):
        if value and value.id in self.context[
            "request"
        ].group.members.values_list("user", flat=True):
            raise ApiException(
                ResponseType.ParamValidationFailed, msg="该成员已在社团中"
            )
        if value and value.id == self.context["request"].group.leader.id:
            raise ApiException(
                ResponseType.ParamValidationFailed, msg="社长无需加入社团"
            )
        return value


class GroupSerializer(serializers.ModelSerializer):
    leader = GroupMemberSerializer(read_only=True)
    members = GroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "introduction",
            "leader",
            "members",
            "create_time",
            "update_time",
        ]

    def create(self, validated_data):
        return Group.objects.create(
            **validated_data,
            leader=self.context["request"].user,
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO: data["activity"] = instance.activity.name
        return data


class GroupInfoSerializer(serializers.ModelSerializer):
    leader = UserInfoSerializer(read_only=True)
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "introduction",
            "leader",
            "favorite",
            "create_time",
            "update_time",
        ]


class NotificationReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationReceiver
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    publisher = serializers.PrimaryKeyRelatedField(
        related_name="publisher",
        label="发布者",
    )

    content = serializers.CharField(label="通知内容")

    receive = serializers.BooleanField(
        label="是否收到",
    )

    receivers = NotificationReceiverSerializer(many=True, read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
