from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=16, unique=True, verbose_name='유저 닉네임')
    address = models.CharField(max_length=128, verbose_name='유저 주소')
    phone = models.CharField(max_length=128, unique=True, verbose_name='유저 전화번호')
    myname = models.CharField(max_length=128, unique=True, verbose_name='이름')

    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural = '유저'

    def __str__(self):
        return self.username