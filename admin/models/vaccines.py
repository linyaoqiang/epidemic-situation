from django.db import models
from django.utils import timezone


class VaccineCompany(models.Model):
    name = models.CharField(verbose_name='疫苗公司',max_length=32)

    def __str__(self):
        return self.name


class VaccineLocation(models.Model):
    name = models.CharField(verbose_name='接种单位',max_length=256)
    def __str__(self):
        return self.name


class Vaccines(models.Model):
    location = models.ForeignKey(verbose_name='疫苗公司', to=VaccineLocation, to_field='id', on_delete=models.CASCADE)
    company = models.ForeignKey(verbose_name='接种单位', to=VaccineCompany, to_field='id', on_delete=models.CASCADE)
    NEEDLES_CHOICES = (
        (1, '第一针'),
        (2, '第二针'),
        (3, '第三针')
    )
    needles = models.IntegerField(verbose_name='针次', choices=NEEDLES_CHOICES)
    quantity = models.IntegerField(verbose_name='数量')
    create_time = models.DateTimeField(verbose_name='发布时间', default=timezone.now)

    