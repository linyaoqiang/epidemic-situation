from admin.models.location import *
from django.db import models
from django.utils import timezone


class Case(models.Model):
    province = models.ForeignKey(verbose_name='省份(自治区)', to=Province, to_field='id',
                                 on_delete=models.CASCADE)
    existing_cases = models.BigIntegerField(verbose_name='现有病例')
    new_cases = models.BigIntegerField(verbose_name='新增病例')
    public_date = models.DateField(verbose_name='发布时间', default=timezone.now)
