from django.shortcuts import render, HttpResponse, redirect
from admin.models.epidemic_situation import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.core import serializers
from django.forms import forms, ModelForm
import json
from admin.utils.access_control import admin_control


class EpidemicSituationModelFrom(ModelForm):
    class Meta:
        model = LocationEpidemicSituation
        fields = ['province', 'city', 'level', 'desc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class EpidemicSituationController:
    @admin_control
    def display(self, request):
        data = request.GET
        page_number = data.get('page')
        page_size = data.get('size')

        if page_number is None or not page_number.isdigit():
            page_number = 1
        else:
            page_number = int(page_number)
        if page_size is None or not page_size.isdigit():
            page_size = 3
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
        paginator = Paginator(es_data, page_size)
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

        return render(request, 'pages/es_display.html', locals())

    @admin_control
    def add_es(self, request):
        form = EpidemicSituationModelFrom()
        return render(request, 'pages/es_edit.html', locals())


    @admin_control
    def update_es(self, request):
        data = request.POST
        form = EpidemicSituationModelFrom(data=data)
        # print(form)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            id = request.POST.get('id')
            areas = request.POST.getlist('areas')
            areas = json.dumps(areas)
            data['areas'] = areas
            if id is None:
                LocationEpidemicSituation.objects.create(**data)
            else:
                LocationEpidemicSituation.objects.filter(id=id).update(**data)
            return redirect('/admin/es/display')
        areas = request.POST.getlist('areas')
        areas = json.loads(areas)
        city_id = request.POST.get('city').id
        return render(request, 'pages/es_edit.html', locals())
    @admin_control
    def edit_es(self, request, id):
        instance = LocationEpidemicSituation.objects.filter(id=id).first()
        form = EpidemicSituationModelFrom(instance=instance)
        areas = instance.areas
        areas = json.loads(areas)
        print(type(areas))
        print(areas)
        city_id = instance.city.id
        return render(request, 'pages/es_edit.html', locals())

    @admin_control
    def delete_es(self, request, id):
        LocationEpidemicSituation.objects.filter(id=id).delete()
        return redirect('/admin/es/display')

