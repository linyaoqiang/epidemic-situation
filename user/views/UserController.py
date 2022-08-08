from django.shortcuts import render, redirect
from user.models import User, HealthReport, UserVaccines
from django.forms.models import model_to_dict
from django.forms import forms, ModelForm
from django.utils import timezone
from admin.utils.paginator import SelfPaginator, EmptyPage
from user.utils.access_control import user_control


class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['password', 'nickname', 'age', 'birth_day', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'layui-input'
            field.widget.attrs['placeholder'] = field.label


class HealthReportModelForm(ModelForm):
    class Meta:
        model = HealthReport
        fields = ['location', 'health_code_status', 'trip_card_status',
                  'vaccination_status', 'error_area', 'body_status', 'health_observations']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'layui-input'
            field.widget.attrs['placeholder'] = field.label


class UserController:
    def index(self, request):
        return redirect('/es')

    def login(self, request):
        if request.method == 'GET':
            return render(request, 'user_template/login.html', locals())

        data = request.POST
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user is None:
            error_message = '用户名或者密码错误'
            return render(request, 'user_template/login.html', locals())

        user = model_to_dict(user)
        del user['birth_day']
        del user['password']
        request.session['user'] = user
        return redirect('/es')

    def register(self, request):
        if request.method == 'GET':
            return render(request, 'user_template/login.html', locals())

        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        if user is not None:
            error_message = '用户名已经被注册了'
            return render(request, 'user_template/login.html', locals())

        user = User.objects.create(username=username, password=password)
        if user is None:
            error_message = '注册失败!'
            return render(request, 'user_template/login.html', locals())
        return redirect('/login')

    @user_control
    def logout(self, request):
        del request.session['user']
        return redirect('/login')

    @user_control
    def user(self, request):
        user = request.session.get('user')
        if request.method == 'GET':
            instance = User.objects.filter(id=user['id']).first()
            if instance is not None:
                form = UserModelForm(instance=instance)
            else:
                form = UserModelForm()
            return render(request, 'user_template/pages/user.html', locals())

        data = request.POST
        form = UserModelForm(data=data)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            change_count = User.objects.filter(id=user['id']).update(**form_cleaned_data)
            if change_count > 0:
                user = User.objects.filter(id=user['id']).first()
                user = model_to_dict(user)
                del user['birth_day']
                del user['password']
                request.session['user'] = user
                message = '更新成功'
                return render(request, 'user_template/pages/user.html', locals())

        message = '更新失败'
        return render(request, 'user_template/pages/user.html', locals())

    @user_control
    def upload_health_report(self, request):
        user = request.session['user']
        if request.method == 'GET':
            health_report = HealthReport.objects.filter(user_id=user['id']).last()
            if health_report is None:
                form = HealthReportModelForm()
            else:
                form = HealthReportModelForm(instance=health_report)

            return render(request, 'user_template/pages/upload_health_report.html', locals())

        data = request.POST
        form = HealthReportModelForm(data=data)
        if form.is_valid():
            form_cleaned_data = form.cleaned_data
            health_report = HealthReport.objects.filter(user_id=user['id'], public_date=timezone.now().date())
            if health_report.count() > 0:
                health_report.update(**form_cleaned_data)
            else:
                form_cleaned_data['user_id'] = user['id']
                HealthReport.objects.create(**form_cleaned_data)
            message = '上报|更新成功'
            return render(request, 'user_template/pages/upload_health_report.html', locals())
        message = '保存失败, 原因未知'
        return render(request, 'user_template/pages/upload_health_report.html', locals())

    @user_control
    def self_vaccines_display(self, request):
        data = request.GET
        page_number = data.get('page')
        page_size = data.get('size')

        if page_number is None or not page_number.isdigit():
            page_number = 1
        else:
            page_number = int(page_number)
        if page_size is None or not page_size.isdigit():
            page_size = 6
        else:
            page_size = int(page_size)

        user = request.session['user']

        user_vaccines_data = UserVaccines.objects.filter(user_id=user['id'])
        paginator = SelfPaginator(user_vaccines_data, page_size, page_number, display_size=11)
        try:
            user_vaccines_list = paginator.page(page_number)
        except EmptyPage as e:
            print(e)
            user_vaccines_list = []
        return render(request, 'user_template/pages/self_vaccines_display.html', locals())
