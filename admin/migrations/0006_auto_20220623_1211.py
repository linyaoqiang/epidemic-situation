# Generated by Django 3.2.13 on 2022-06-23 04:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0005_vaccinecompany_vaccinelocation_vaccines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccines',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 23, 4, 11, 52, 655499, tzinfo=utc), verbose_name='发布时间'),
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('existing_cases', models.BigIntegerField(verbose_name='现有病例')),
                ('new_cases', models.BigIntegerField(verbose_name='新增病例')),
                ('public_date', models.DateField(default=datetime.datetime(2022, 6, 23, 4, 11, 52, 667501, tzinfo=utc), verbose_name='发布时间')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin.province', verbose_name='省份(自治区)')),
            ],
        ),
    ]
