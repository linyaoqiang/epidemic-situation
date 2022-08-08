from django.shortcuts import render, HttpResponse, redirect
from admin.models.area_policy import *
from admin.utils.paginator import SelfPaginator
from django.http import JsonResponse
from django.core import serializers
from django.forms import forms, ModelForm, CharField
from django.core.validators import RegexValidator
import json
import time

from admin.utils.access_control import admin_control

class AreaPolicyModelForm(ModelForm):
    class Meta:
        model = AreaPolicy
        fields = ['area', 'epidemic_prevention_policy', 'travel_policy', 'psychological_hotline']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class AreaOutpatientDepartmentModelForm(ModelForm):
    class Meta:
        model = AreaOutpatientDepartment
        fields = ['area', 'name', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class AreaPolicyPaginator(SelfPaginator):
    pass


class OutpatientDepartmentPaginator(SelfPaginator):
    pass


class AreaPolicyController:

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
            page_size = 8
        else:
            page_size = int(page_size)

        area_id = data.get('a_id')

        filter_condition = {}

        if area_id is not None and area_id != '' and area_id.isdigit():
            area_id = int(area_id)
            filter_condition['area_id'] = area_id
            area = Area.objects.filter(id=area_id).first()
            city = area.city
            province = city.province
        else:
            area_id = ''

        area_policy_data = AreaPolicy.objects.filter(**filter_condition)
        paginator = AreaPolicyPaginator(area_policy_data, page_size, page_number, display_size=11)
        area_policies = paginator.page(page_number)
        provinces = Province.objects.all()

        return render(request, 'pages/area_policy_display.html', locals())

    @admin_control
    def edit(self, request, area_policy_id):
        area_policy = AreaPolicy.objects.filter(id=area_policy_id).first()
        form = AreaPolicyModelForm(instance=area_policy)
        provinces = Province.objects.all()
        cities = City.objects.all()
        area = area_policy.area
        city = area.city
        province = city.province
        return render(request, 'pages/area_policy_edit.html', locals())


    def insert_test(self, request):
        areas = Area.objects.all()
        for area in areas:
            area_id = area.id
            AreaPolicy.objects.create(area_id=area_id)
        return HttpResponse('OK')

    @admin_control
    def update(self, request):
        data = request.POST
        form = AreaPolicyModelForm(data=data)
        area_policy_id = data.get('id')
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            if area_policy_id is None:
                AreaPolicy.objects.create(**form_cleaned_data)
            else:
                AreaPolicy.objects.filter(id=area_policy_id).update(**form_cleaned_data)
            return redirect('/admin/area_policy/display')
        return render(request, 'pages/area_policy_edit.html', locals())

    @admin_control
    def outpatient_department_display(self, request):
        data = request.GET
        page_number = data.get('page')
        page_size = data.get('size')

        if page_number is None or not page_number.isdigit():
            page_number = 1
        else:
            page_number = int(page_number)
        if page_size is None or not page_size.isdigit():
            page_size = 4
        else:
            page_size = int(page_size)

        area_id = data.get('a_id')
        filter_condition = {}

        if area_id is not None and area_id != '' and area_id.isdigit():
            area_id = int(area_id)
            filter_condition['area_id'] = area_id
            area = Area.objects.filter(id=area_id).first()
            city = area.city
            province = city.province
        else:
            area_id = ''

        outpatient_department_data = AreaOutpatientDepartment.objects.filter(**filter_condition)
        paginator = OutpatientDepartmentPaginator(outpatient_department_data, page_size, page_number, display_size=11)
        if paginator.count >= 1:
            outpatient_departments = paginator.page(page_number)
        else:
            outpatient_departments = []
        provinces = Province.objects.all()

        return render(request, 'pages/area_policy/outpatient_department_display.html', locals())

    @admin_control
    def outpatient_department_add(self, request):
        form = AreaOutpatientDepartmentModelForm()
        provinces = Province.objects.all()
        cities = City.objects.all()

        area_id = request.GET.get('a_id')
        if area_id is not None and area_id.isdigit():
            area = Area.objects.filter(id=area_id).first()
            city = area.city
            province = city.province
        return render(request, 'pages/area_policy/outpatient_department_edit.html', locals())

    @admin_control
    def outpatient_department_edit(self, request, out_depart_id):
        out_depart = AreaOutpatientDepartment.objects.filter(id=out_depart_id).first()
        form = AreaOutpatientDepartmentModelForm(instance=out_depart)
        provinces = Province.objects.all()
        cities = City.objects.all()
        area = out_depart.area
        city = area.city
        province = city.province
        return render(request, 'pages/area_policy/outpatient_department_edit.html', locals())

    @admin_control
    def outpatient_department_update(self, request):
        data = request.POST
        form = AreaOutpatientDepartmentModelForm(data=data)
        out_depart_id = data.get('id')
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            if out_depart_id is None:
                AreaOutpatientDepartment.objects.create(**form_cleaned_data)
            else:
                AreaOutpatientDepartment.objects.filter(id=out_depart_id).update(**form_cleaned_data)
            return redirect('/admin/area_policy/outpatient_department/display')
        return render(request, 'pages/area_policy/outpatient_department_edit.html', locals())
