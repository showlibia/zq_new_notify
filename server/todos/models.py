from django.db import models
from django.utils import timezone
# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextFeild(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reminder = models.DateTimeField(null=True,blank=True)
    deadline = models.DateTimeField(null=True, blank=True) 

    def __str__(self):  
        return self.title