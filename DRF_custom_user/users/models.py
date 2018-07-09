from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 以下可加入想要的字段
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.username # 这里是AbstractUser里面定义好的