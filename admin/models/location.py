from django.db import models


class Province(models.Model):
    name = models.CharField(verbose_name='省份名称', max_length=32)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(verbose_name='城市名称', max_length=32)
    province = models.ForeignKey(verbose_name='省份ID', to=Province, to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(verbose_name='地区名称', max_length=32)
    city = models.ForeignKey(verbose_name='城市ID', to=City, to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.name