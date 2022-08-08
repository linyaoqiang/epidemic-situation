from django.shortcuts import render, HttpResponse, redirect
from admin.models.case import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.core import serializers
from django.forms import forms, ModelForm
import json
import time
from admin.utils.access_control import admin_control


class CaseModelForm(ModelForm):
    class Meta:
        model = Case
        fields = ['province', 'existing_cases', 'new_cases']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False


class CaseController:
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

        where_template = []

        province_id = data.get('p_id')
        if province_id is not None and province_id != '' and province_id.isdigit():
            province_id = int(province_id)
            where_template.append('province_id = {}'.format(province_id))
        else:
            province_id = ''

        previous_date = data.get('p_date')
        if previous_date is not None and previous_date != '' and is_valid_date(previous_date) and previous_date <= timezone.now().date().__str__():
            where_template.append('public_date >= "{}"'.format(previous_date))
        else:
            previous_date = ''

        next_date = data.get('n_date')
        if next_date is not None and next_date != '' and is_valid_date(next_date) and next_date <= timezone.now().date().__str__():
           where_template.append('public_date <= "{}"'.format(next_date))
        else:
            next_date = ''

        case_data = Case.objects.extra(where=where_template)
        paginator = Paginator(case_data, page_size)
        cases = paginator.page(page_number)
        provinces = Province.objects.all()
        now_date = timezone.now().date()
        return render(request, 'pages/case_display.html', locals())

    @admin_control
    def edit(self, request):
        data = request.GET
        province_id = data.get('p_id')
        instance = None
        form_data = {}
        print(timezone.now().date())
        if province_id != None and province_id.isdigit():
            instance = Case.objects.filter(province_id=province_id,
                                           public_date=timezone.now().date()).first()
            form_data['province'] = Province.objects.filter(id=province_id).first()
        else:
            province_id = ''
        if instance is not None:
            form = CaseModelForm(instance=instance)
        else:
            form = CaseModelForm(data=form_data)
        return render(request, 'pages/case_edit.html', locals())
    @admin_control
    def update(self, request):
        data = request.POST
        form = CaseModelForm(data=data)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            province = form_cleaned_data.get('province')
            print(type(province))
            instance_queryset = Case.objects.filter(province=province, public_date=timezone.now().date())
            instance = instance_queryset.first()
            if instance is not None:
                instance_queryset.update(**form_cleaned_data)
            else:
                Case.objects.create(**form_cleaned_data)
            return redirect('/admin/case/display')
        province_id = form.cleaned_data.get('province')
        print(province_id)
        return redirect('/admin/case/edit?p_id={}'.format(province_id))


    @admin_control
    def fetch_case(self,request, province_id):
        cases = Case.objects.filter(province_id=province_id, public_date=timezone.now().date())
        result = serializers.serialize('json', queryset=cases)
        return JsonResponse(result, safe=False)