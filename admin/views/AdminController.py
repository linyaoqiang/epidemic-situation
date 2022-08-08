from django.shortcuts import render, HttpResponse
import json
import os
import requests
from django.shortcuts import render, redirect
from requests.adapters import HTTPAdapter
from admin.models.location import *
from admin.models.user import *
from admin.utils.access_control import admin_control
from django.forms.models import model_to_dict


class AdminController:

    def index(self,request):
        return redirect('/admin/es/display')

    def login(self, request, *args):
        next_location = ''
        if request.method == 'GET':
            next_location = request.GET.get('next')
            if next_location is None or next_location == '':
                next_location = '/admin/es/display'
            return render(request, 'login.html', locals())

        data = request.POST
        next_location = request.GET.get('next')
        username = data.get('username')
        password = data.get('password')
        print(next_location)
        user = User.objects.filter(username=username, password=password).first()
        if user is not None:
            if user.power == 2:
                login_error = '当前用户无权访问管理界面'
                return render(request, 'login.html', locals())
            else:
                user = model_to_dict(user)
                print(user)
                request.session['admin'] = user
                user['birth_day'] = str(user['birth_day'])
                if next_location is None or next_location == '':
                    next_location = '/admin/es/display'
                return redirect(next_location)
        login_error = '用户名或者密码错误'
        return render(request, 'login.html', locals())

    @admin_control
    def logout(self, request):
        del request.session['admin']
        return redirect('/admin/login')

    def menu(self):
        file_dir = os.path.dirname(__file__)  # 当前文件所在的目录
        file_path = os.path.join(file_dir, 'static/json/menu.json')
        print(file_path)
        with open(file_path, mode='r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def test(self, request):

        session = requests.Session()
        # 重试次数为3
        session.mount('http://', HTTPAdapter(max_retries=10))
        session.mount('https://', HTTPAdapter(max_retries=10))
        # 超时时间为5s
        session.get('http://example.com', timeout=10)

        api = 'http://guolin.tech/api/china/'
        response = session.get(api)
        data = response.json()
        for item in data:
            item_value = item.pop('id')
            Province.objects.create(**item)
            api_2 = "{}{}".format(api, item_value)
            sub_data = session.get(api_2).json()
            for sub_item in sub_data:
                sub_item_value = sub_item.pop('id')
                sub_item['province_id'] = item_value
                City.objects.create(**sub_item)

        return HttpResponse('HELLO')

    def test2(self, request):
        session = requests.Session()
        # 重试次数为3
        session.mount('http://', HTTPAdapter(max_retries=10))
        session.mount('https://', HTTPAdapter(max_retries=10))
        # 超时时间为5s
        session.get('http://example.com', timeout=10)

        data = City.objects.all()
        api = 'http://guolin.tech/api/china/{}/{}'
        for item in data:
            array = session.get(api.format(item.province.id, item.id)).json()
            for sub_item in array:
                sub_item['city_id'] = item.id
                sub_item.pop('weather_id')
                Area.objects.create(**sub_item)

        return HttpResponse('OK')
