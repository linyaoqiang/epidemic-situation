from django.shortcuts import render, HttpResponse, redirect
from admin.models.vaccines import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.core import serializers
from django.forms import forms, ModelForm
import json
from admin.utils.access_control import admin_control



class VaccinesModelForm(ModelForm):
    class Meta:
        model = Vaccines
        fields = ['company', 'location', 'needles', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class VaccinesController:
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

        company_id = data.get('c_id')
        location_id = data.get('l_id')
        filter_condition = {}
        if company_id is not None and company_id != '' and company_id.isdigit():
            company_id = int(company_id)
            filter_condition['company_id'] = company_id
        else:
            company_id = ''
        if location_id is not None and location_id != '' and location_id.isdigit():
            location_id = int(location_id)
            filter_condition['location_id'] = location_id
        else:
            location_id = ''

        vaccines_data = Vaccines.objects.filter(**filter_condition)
        paginator = Paginator(vaccines_data, page_size)
        vaccines_list = paginator.page(page_number)
        vaccines_companies = VaccineCompany.objects.all()
        vaccines_locations = VaccineLocation.objects.all()
        return render(request, 'pages/vaccines_display.html', locals())

    @admin_control
    def add(self, request):
        form = VaccinesModelForm()
        return render(request, 'pages/vaccines_edit.html', locals())

    @admin_control
    def update(self, request):
        data = request.POST
        form = VaccinesModelForm(data=data)
        vaccines_id = data.get('id')
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            if vaccines_id is None:
                Vaccines.objects.create(**form_cleaned_data)
            else:
                Vaccines.objects.filter(id=vaccines_id).update(**form_cleaned_data)
            return redirect('/admin/vaccines/display')
        return render(request, 'pages/vaccines_edit.html', locals())
    @admin_control
    def edit(self, request, vaccines_id):
        instance = Vaccines.objects.filter(id=vaccines_id).first()

        form = VaccinesModelForm(instance=instance)
        return render(request, 'pages/vaccines_edit.html', locals())
    @admin_control
    def delete(self, request, vaccines_id):
        Vaccines.objects.filter(id=vaccines_id).delete()
        return redirect('/admin/vaccines/display')

    def test(self, request):
        print(Vaccines.objects.all().count())
        return HttpResponse('OK')
