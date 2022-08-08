# Generated by Django 3.2.13 on 2022-06-23 12:58

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0011_auto_20220623_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='用户密码')),
                ('nickname', models.CharField(default=uuid.UUID('8874b01a-7d01-4030-9119-5a63af5d03ac'), max_length=32, verbose_name='昵称')),
                ('age', models.IntegerField(default=0, verbose_name='年龄')),
                ('birth_day', models.DateField(default=django.utils.timezone.now, verbose_name='生日')),
                ('gender', models.IntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别')),
                ('status', models.IntegerField(choices=[(1, '正常使用'), (2, '封号中')], default=1, verbose_name='账户状态')),
                ('power', models.IntegerField(choices=[(1, '管理员'), (2, '普通用户')], default=2, verbose_name='账户类型')),
            ],
        ),
    ]