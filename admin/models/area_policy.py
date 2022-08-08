from admin.models.location import *
from django.db import models
from django.utils import timezone


class AreaOutpatientDepartment(models.Model):
    area = models.ForeignKey(verbose_name='地区', to=Area, to_field='id', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='门诊名称', max_length=32)
    location = models.CharField(verbose_name='门诊地区', max_length=256)


class AreaPolicy(models.Model):
    area = models.ForeignKey(verbose_name='地区', to=Area, to_field='id', on_delete=models.CASCADE)
    epidemic_prevention_policy = models.TextField(verbose_name='防疫政策', null=True, blank=True)
    travel_policy = models.TextField(verbose_name='出行政策', null=True, blank=True)
    psychological_hotline = models.CharField(verbose_name='心理热线', max_length=32, null=True, blank=True)