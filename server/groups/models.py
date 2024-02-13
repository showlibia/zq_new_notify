from django.db import models

# Create your models here.
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