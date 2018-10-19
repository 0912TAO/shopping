from django.db import models

# Create your models here.


# 引入内置user表
from django.contrib.auth.models import User


# 用户数据
class UserA(models.Model):
    uid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11,verbose_name='用户电话')
    umaney = models.CharField(max_length=255, verbose_name="用户余额")
    age = models.IntegerField(default=18, verbose_name='用户年龄')
    gender = models.CharField(max_length=18, verbose_name='用户性别')
    herder = models.ImageField(upload_to="static/img/headers",default="static/images/1(1).jpeg",verbose_name='用户头像')
    # 默认是0表示保密，1表示男生，2表示女生
    collection =models.CharField(max_length=255, verbose_name="用户收藏店铺")
    add = models.CharField(max_length=500,verbose_name="用户收货地址")

    user = models.OneToOneField(User,on_delete=models.CASCADE)