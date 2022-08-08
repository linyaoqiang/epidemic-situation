from admin.models.location import *
from django.db import models


class LocationEpidemicSituation(models.Model):
    province = models.ForeignKey(verbose_name='省份', to=Province, to_field='id', on_delete=models.CASCADE)
    city = models.ForeignKey(verbose_name='城市', to=City, to_field='id',
                             null=True, blank=True, on_delete=models.CASCADE)
    areas = models.CharField(verbose_name='区域集合', max_length=256)

    LEVEL_CHOICES = (
        (1, '中风险地区'),
        (2, '高风险地区')
    )

    level = models.IntegerField(verbose_name='风险地区类型', choices=LEVEL_CHOICES)

    desc = models.TextField(verbose_name='风险地区描述')


    def __setitem__(self, key, value):
        self.key = value
