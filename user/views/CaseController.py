from user.models import *
from django.db.models import Sum
from django.shortcuts import render
from admin.utils.paginator import SelfPaginator, EmptyPage
import time


class CasePaginator(SelfPaginator):
    pass

def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False


class CaseController:
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

        case_data = Case.objects.extra(where=where_template)
        paginator = CasePaginator(case_data, page_size, page_number, display_size=11)
        try:
            cases = paginator.page(page_number)
        except EmptyPage as e:
            print(e)
            cases = []
        provinces = Province.objects.all()
        now_date = timezone.now().date()
        case_displaying = 'layui-this'

        national_cases = Case.objects.filter(public_date=timezone.now().date()).aggregate(Sum('existing_cases'), Sum('new_cases'))

        national_existing_cases = national_cases.get('existing_cases__sum')
        national_new_cases = national_cases.get('new_cases__sum')

        return render(request, 'user_template/pages/case_display.html', locals())