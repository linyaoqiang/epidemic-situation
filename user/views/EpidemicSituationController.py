from user.models import *
from django.shortcuts import render
from admin.utils.paginator import SelfPaginator
import json


class EpidemicSituationPaginator(SelfPaginator):
    pass


class EpidemicSituationController:
    def display(self, request):
        data = request.GET
        page_number = data.get('page')
        page_size = data.get('size')

        if page_number is None or not page_number.isdigit():
            page_number = 1
        else:
            page_number = int(page_number)
        if page_size is None or not page_size.isdigit():
            page_size = 2
        else:
            page_size = int(page_size)

        province_id = data.get('p_id')
        city_id = data.get('c_id')
        filter_condition = {}
        if province_id is not None and province_id != '' and province_id.isdigit():
            province_id = int(province_id)
            filter_condition['province_id'] = province_id
        else:
            province_id = ''
        if city_id is not None and city_id != '' and city_id.isdigit():
            city_id = int(city_id)
            filter_condition['city_id'] = city_id
        else:
            city_id = ''

        es_data = LocationEpidemicSituation.objects.filter(**filter_condition)
        paginator = EpidemicSituationPaginator(es_data, page_size, page_number, display_size=11)

        if paginator.count <= 0:
            objects = []
        else:
            objects = paginator.page(page_number)

        for item in objects:
            ids = ''
            for value in json.loads(item.areas):
                ids += '{}, '.format(value)
            if ids != '' and len(ids) >= 3:
                ids = ids[:len(ids) - 2]
                item.areas_object = Area.objects.extra(where=['id in ({})'.format(ids)])
                print(item.areas_object)
        provinces = Province.objects.all()

        es_displaying = 'layui-this'

        return render(request, 'user_template/pages/es_display.html', locals())
