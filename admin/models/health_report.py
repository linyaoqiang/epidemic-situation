from admin.models.user import *
from django.db import models


class HealthReport(models.Model):
    user = models.ForeignKey(verbose_name='用户', to=User, to_field='id', on_delete=models.CASCADE)
    location = models.CharField(verbose_name='本人当前所在位置', max_length=256)
    
    HEALTH_CODE_STATUS_CHOICES = (
        (1, '绿码'),
        (2, '黄码'),
        (3, '红码')

    )
    health_code_status = models.IntegerField(verbose_name='当前健康码状态', choices=HEALTH_CODE_STATUS_CHOICES, default=1)

    TRIP_CARD_STATUS_CHOICES = (
        (1, '否'),
        (2, '是')
    )

    trip_card_status = models.IntegerField(verbose_name='本人大数据行程卡是否带"*"', choices=TRIP_CARD_STATUS_CHOICES, default=1)

    VACCINATION_STATUS_CHOICES = (
        (1, '已经接种三针'),
        (2, '已经接种二针'),
        (3, '已经接种一针'),
        (4, '未接种'),
    )

    vaccination_status = models.IntegerField(verbose_name='接种新冠疫苗情况', choices=VACCINATION_STATUS_CHOICES, default=1)

    ERROR_AREA_CHOICES = (
        (1, '否'),
        (2, '是')
    )

    error_area = models.IntegerField(verbose_name='当日是否14天内到达过中高风险地区?', choices=ERROR_AREA_CHOICES, default=1)

    IS_FEVER_CHOICES = (
        (1, '否'),
        (2, '是')
    )

    is_fever = models.IntegerField(verbose_name='今日是否出现发热情况?(腋温≥37.3℃)', choices=IS_FEVER_CHOICES, default=1)

    BODY_STATUS_CHOICES = (
        (1, '正常'),
        (2, '干咳、乏力、 嗅觉味觉退减、鼻、咽痛、结膜炎、肌痛和腹泻任一症状'),
        (3, '其他')
    )

    body_status = models.IntegerField(verbose_name='目前身体状态', choices=BODY_STATUS_CHOICES, default=1)

    HEALTH_OBSERVATIONS_CHOICES = (
        (1, '无需观察'),
        (2, '自我健康监测'),
        (3, '居家健康检测'),
        (4, '医学居家隔离'),
        
        (5, '医学集中隔离(在政府规定的酒店或医院灯场所集中健康观察)')
    )

    health_observations = models.IntegerField(verbose_name='目前健康观察情况为', choices=HEALTH_OBSERVATIONS_CHOICES, default=1)
    public_date = models.DateField(verbose_name='发布时间', default=timezone.now)


