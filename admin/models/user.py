from django.db import models
from admin.models.vaccines import Vaccines
from django.utils import timezone
import uuid


class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=128)
    password = models.CharField(verbose_name='用户密码', max_length=128)

    nickname = models.CharField(verbose_name='昵称', max_length=128, default=uuid.uuid4())
    age = models.IntegerField(verbose_name='年龄', default=0)
    birth_day = models.DateField(verbose_name='生日', default=timezone.now)

    GENDER_CHOICE = (
        (1, '男'),
        (2, '女')
    )

    gender = models.IntegerField(verbose_name='性别', choices=GENDER_CHOICE, default=1)

    STATUS_CHOICE = (
        (1, '正常使用'),
        (2, '封号中')
    )
    status = models.IntegerField(verbose_name='账户状态', choices=STATUS_CHOICE, default=1)

    POWER_CHOICE = (
        (1, '管理员'),
        (2, '普通用户')
    )
    power = models.IntegerField(verbose_name='账户类型', choices=POWER_CHOICE, default=2)


class UserVaccines(models.Model):
    user = models.ForeignKey(verbose_name='预约用户', to=User, to_field='id', on_delete=models.CASCADE)
    vaccines = models.ForeignKey(verbose_name='疫苗', to=Vaccines, to_field='id', on_delete=models.CASCADE)
    time_of_appointment = models.DateField(verbose_name='预约时间', default=timezone.now)
