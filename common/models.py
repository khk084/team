from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name='유저 아이디')
    password = models.CharField(max_length=128, verbose_name='유저 비밀번호')
    nickname = models.CharField(max_length=16, unique=True, verbose_name='유저 닉네임')
    email = models.EmailField(max_length=128, unique=True, verbose_name='유저 이메일')
    address = models.CharField(max_length=128, verbose_name='유저 주소')
    phone = models.CharField(max_length=128, unique=True, verbose_name='유저 전화번호')


class Meta:
    db_table = 'user'
    verbose_name = '유저'
    verbose_name_plural = '유저'

def __str__(self):
    return self.username