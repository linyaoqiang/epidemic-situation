from django.shortcuts import render, HttpResponse, redirect
from user.models import Area, AreaPolicy, AreaOutpatientDepartment, Province, City
from admin.utils.paginator import SelfPaginator
from user.utils.access_control import user_control

class AreaPolicyController:
    @user_control
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
        paginator = SelfPaginator(area_policy_data, page_size, page_number, display_size=11)
        area_policies = paginator.page(page_number)
        provinces = Province.objects.all()

        return render(request, 'user_template/pages/area_policy_display.html', locals())

    @user_control
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
        paginator = SelfPaginator(outpatient_department_data, page_size, page_number, display_size=11)
        if paginator.count >= 1:
            outpatient_departments = paginator.page(page_number)
        else:
            outpatient_departments = []
        provinces = City.objects.all()

        return render(request, 'user_template/pages/outpatient_department_display.html', locals())
