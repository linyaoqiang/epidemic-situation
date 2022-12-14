# Generated by Django 3.2.13 on 2022-06-23 14:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0012_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default=uuid.UUID('7a9763b8-66e2-4a9c-9294-c5980b0ac126'), max_length=128, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='用户密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=128, verbose_name='用户名'),
        ),
    ]
