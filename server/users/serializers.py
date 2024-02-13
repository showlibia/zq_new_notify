from rest_framework import serializers
from .models import User
from groups.models import Group
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        slug_field='name',  # 假设Group模型中有一个'name'字段用于表示群组名
        required=False
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'phone',
            'wechat',
            'school_number',
            'avatar',
            'gender',
            'groups',
            'is_authenticated',
            'openid',
            'union_id'
        ]
        read_only_fields = ('is_authenticated',)  # 如果你希望某些字段在API中是只读的

    def validate_username(self, value):
        """
        Validate the length of the username.
        """
        if len(value) > 20:
            raise serializers.ValidationError("昵称不能超过20个字符")
        return value

    def validate_avatar(self, value):
        """
        Validate and compress the avatar image.
        """
        if value:
            if value.size > 1024 * 1024 * 4:
                raise serializers.ValidationError("头像文件大小不能超过4MB")

            img = Image.open(value)
            output = BytesIO()

            img.thumbnail((300, 300))

            if img.format != 'JPEG':
                img = img.convert('RGB')

            img.save(output, format='JPEG', quality=70)
            output.seek(0)

            value = InMemoryUploadedFile(
                output,
                'ImageField',
                "%s.jpg" % value.name.split('.')[0],
                'image/jpeg',
                output.tell(),
                None
            )

        return value

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'phone',
            'wechat',
            'school_number',
            'avatar',
            'gender',
            'groups',
        ]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['groups'] = [group.name for group in data['groups']]
        return data