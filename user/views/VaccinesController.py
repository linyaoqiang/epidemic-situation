from user.models import Vaccines, VaccineCompany, VaccineLocation, UserVaccines, User
from django.db.models import Sum
from django.shortcuts import render
from admin.utils.paginator import SelfPaginator, EmptyPage
from django.http import JsonResponse
import json
from user.utils.access_control import user_control

class VaccinesController:

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
        paginator = SelfPaginator(vaccines_data, page_size, page_number, display_size=11)
        vaccines_list = paginator.page(page_number)
        vaccines_companies = VaccineCompany.objects.all()
        vaccines_locations = VaccineLocation.objects.all()

        user = request.session.get('user')
        user_vaccines_list = UserVaccines.objects.filter(user_id=user['id'])
        already_vaccines_ids = []
        for item in user_vaccines_list:
            already_vaccines_ids.append(item.vaccines.id)
        return render(request, 'user_template/pages/vaccines_display.html', locals())

    @user_control
    def make_vaccines(self, request, vaccines_id):
        user = request.session.get('user')
        user_vaccines = UserVaccines.objects.filter(user_id=user['id'], vaccines_id=vaccines_id).first()
        if user_vaccines is not None:
            error = {'status': 500, 'message': '已经预约过该疫苗'}
            return JsonResponse(json.dumps(error), safe=False)

        vaccines = Vaccines.objects.filter(id=vaccines_id).first()
        if vaccines is None:
            error = {'status': 400, 'message': '疫苗不存在'}
            return JsonResponse(json.dumps(error), safe=False)

        if vaccines.quantity <= 0:
            error = {'status': 401, 'message': '疫苗数量不足'}
            return JsonResponse(json.dumps(error), safe=False)

        user_vaccines = UserVaccines.objects.create(user_id=user['id'], vaccines_id=vaccines_id)

        if user_vaccines is None:
            error = {'status': 402, 'message': '预约疫苗失败'}
            return JsonResponse(json.dumps(error), safe=False)

        quantity = vaccines.quantity - 1
        Vaccines.objects.filter(id=vaccines_id).update(quantity=quantity)
        data = {'status': 200, 'message': '预约疫苗成功'}
        return JsonResponse(json.dumps(data), safe=False)

