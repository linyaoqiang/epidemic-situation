# Generated by Django 3.2.13 on 2022-06-23 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0009_auto_20220623_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epidemic_prevention_policy', models.TextField(verbose_name='防疫政策')),
                ('travel_policy', models.TextField(verbose_name='出行政策')),
                ('psychological_hotline', models.CharField(max_length=32, verbose_name='心理热线')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.area', verbose_name='地区')),
            ],
        ),
        migrations.CreateModel(
            name='AreaOutpatientDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='门诊名称')),
                ('location', models.CharField(max_length=256, verbose_name='门诊地区')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.area', verbose_name='地区')),
            ],
        ),
    ]