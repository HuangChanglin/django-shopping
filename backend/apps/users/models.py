from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField('手机号', max_length=11, unique=True, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=[
        ('male', '男'), ('female', '女'), ('unknown', '未知')
    ], default='unknown')
    birthday = models.DateField('生日', null=True, blank=True)
    address = models.TextField('收货地址', blank=True)
    balance = models.DecimalField('账户余额', max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
