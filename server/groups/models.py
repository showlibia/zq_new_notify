from django.db import models

# Create your models here.
class Member(models.Model):
    def _init_(self,id,name,avatar):
        self.id = id
        self.name = name
        self.avatar = avatar

class Group(models.Model):
    def _init_(self,avatar_image,name,description):
        self.avatar_image = avatar_image
        self.name = name
        self.description = description
        self.members = []

    def add_member(self,member):
        self.members.append(member)

    def remove_member(self,member):
        if member in self.members:
            self.members.remove(member)
        else:
            print("未发现此成员。")

class Notification(models.Model):
    """
    通知
    """
    publisher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="publisher",
        verbose_name="发布者",
    )

    content = models.TextField(verbose_name="通知内容")

    class Meta:
        app_label = "groups"
        db_table = "zq_notify_group"
        verbose_name = "通知"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.content}"


class Attendance(models.Model):
    """
    签到
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="签到成员",
    )

    attendance = models.BooleanField(
        default=False
    )

# Create your models here.
