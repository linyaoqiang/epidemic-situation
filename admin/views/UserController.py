from django.shortcuts import render, redirect
from admin.models.health_report import *
from admin.utils.paginator import SelfPaginator
from django.forms import forms, ModelForm
from admin.utils.model_fiield import resolve_model_fields
from admin.utils.access_control import admin_control
import time


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'age', 'birth_day', 'gender', 'status', 'power']

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


class UserPaginator(SelfPaginator):
    pass


class HealthReportPaginator(SelfPaginator):
    pass


class UserController:
    @admin_control
    def display(self, request):
        data = request.GET
        where_template = []
        nickname = data.get('nick')
        if nickname is None:
            nickname = ''
        where_template.append('nickname like "%{0}%"'.format(nickname))

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

        previous_date = data.get('p_date')
        if previous_date is not None and previous_date != '' and is_valid_date(
                previous_date) and previous_date <= timezone.now().date().__str__():
            where_template.append('birth_day >= "{}"'.format(previous_date))
        else:
            previous_date = ''

        next_date = data.get('n_date')
        if next_date is not None and next_date != '' and is_valid_date(
                next_date) and next_date <= timezone.now().date().__str__():
            where_template.append('birth_day <= "{}"'.format(next_date))
        else:
            next_date = ''

        user_data = User.objects.extra(where=where_template)
        paginator = UserPaginator(user_data, page_size, page_number, display_size=11)
        if paginator.count >= 1:
            users = paginator.page(page_number)
        else:
            users = []

        return render(request, 'pages/user_display.html', locals())

    @admin_control
    def add(self, request):
        form = UserModelForm()
        return render(request, 'pages/user_edit.html', locals())

    @admin_control
    def edit(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        form = UserModelForm(instance=user)
        user_id = user_id
        return render(request, 'pages/user_edit.html', locals())
    @admin_control
    def update(self, request):
        data = request.POST
        form = UserModelForm(data=data)
        user_id = data.get('id')
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            if user_id is not None and user_id.isdigit():
                User.objects.filter(id=user_id).update(**form_cleaned_data)
            else:
                user_flag = User.objects.filter(username=form_cleaned_data.get('username'))
                if not user_flag:
                    User.objects.create(**form_cleaned_data)
                else:
                    username_exist_error = '用户名已经存在'
                    return render(request, 'pages/user_edit.html', locals())

            return redirect('/admin/user/display')
        return render(request, 'pages/user_edit.html', locals())

    @admin_control
    def health_report_display(self, request):
        data = request.GET
        where_template = []

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

        previous_date = data.get('p_date')
        if previous_date is not None and previous_date != '' and is_valid_date(
                previous_date) and previous_date <= timezone.now().date().__str__():
            where_template.append('public_date >= "{}"'.format(previous_date))
        else:
            previous_date = ''

        next_date = data.get('n_date')
        if next_date is not None and next_date != '' and is_valid_date(
                next_date) and next_date <= timezone.now().date().__str__():
            where_template.append('public_date <= "{}"'.format(next_date))
        else:
            next_date = ''

        health_report_data = HealthReport.objects.extra(where=where_template)
        paginator = HealthReportPaginator(health_report_data, page_size, page_number, display_size=11)
        if paginator.count >= 1:
            health_reports = paginator.page(page_number)
        else:
            health_reports = []

        health_report_fields = resolve_model_fields('admin', 'HealthReport')
        health_report_fields.pop('id')
        now_str = timezone.now().date().__str__()
        return render(request, 'pages/health_report_display.html', locals())
