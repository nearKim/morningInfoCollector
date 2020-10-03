from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class SimpleUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    kakao_user_token = models.CharField(max_length=100, null=True)
    kakao_refresh_token = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = "email"
