from django.db import models
from groups.models import Group
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    基本用户表
    """
    username = models.CharField("用户名", max_length=150, unique=True)
    phone = models.CharField(max_length=13, default="", verbose_name="手机")
    wechat = models.CharField(max_length=25, default="", verbose_name="wechat")
    school_number = models.CharField(max_length=20, default="", verbose_name="学号")

    # 个性化信息
    avatar = models.ImageField(
        upload_to="avatar",
        default=r"avatar\\default.jpg",
        verbose_name="头像"
    )
    gender = models.IntegerField(
        choices=(
            (0, "未知"),
            (1, "男"),
            (2, "女")
        ),
        verbose_name="性别",
    )

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="members",
        verbose_name="加入的社团"
    )

    # 认证
    is_authenticated = models.BooleanField("是否激活", default=True)
    openid = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        verbose_name="微信openid"
    )
    union_id = models.UUIDField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="自强union_id"
    )

    class Meta:
        app_label = "users"
        db_table = "zq_notify_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username