from django.urls import path
from admin.views.AdminController import *
from admin.views.LocationController import *
from admin.views.EpidemicSituationController import *
from admin.views.VaccinesController import *
from admin.views.CaseController import *
from admin.views.AreaPolicyController import *
from admin.views.UserController import *

admin_controller = AdminController()
location_controller = LocationController()
epidemic_situation_controller = EpidemicSituationController()
vaccines_controller = VaccinesController()
case_controller = CaseController()
area_policy_controller = AreaPolicyController()
user_controller = UserController()

urlpatterns = [
    path('admin/', admin_controller.index),
    path('admin/login', admin_controller.login),
    path('admin/logout', admin_controller.logout),
    path('admin/location/<int:province_id>', location_controller.get_city),
    path('admin/location/<int:province_id>/<int:city_id>', location_controller.get_areas),
    path('admin/location/fetch/city/<int:city_id>', location_controller.get_areas),

    path('admin/es/add', epidemic_situation_controller.add_es),
    path('admin/es/display', epidemic_situation_controller.display),
    path('admin/es/update', epidemic_situation_controller.update_es),
    path('admin/es/edit/<int:id>', epidemic_situation_controller.edit_es),
    path('admin/es/delete/<int:id>', epidemic_situation_controller.delete_es),

    path('admin/vaccines/display', vaccines_controller.display),
    path('admin/vaccines/add', vaccines_controller.add),
    path('admin/vaccines/update', vaccines_controller.update),
    path('admin/vaccines/edit/<int:vaccines_id>', vaccines_controller.edit),
    path('admin/vaccines/delete/<int:vaccines_id>', vaccines_controller.delete),

    path('admin/case/display', case_controller.display),
    path('admin/case/edit', case_controller.edit),
    path('admin/case/update', case_controller.update),
    path('admin/case/fetch/<int:province_id>', case_controller.fetch_case),

    path('admin/area_policy/display', area_policy_controller.display),
    path('admin/area_policy/edit/<int:area_policy_id>', area_policy_controller.edit),
    path('admin/area_policy/update', area_policy_controller.update),


    path('admin/area_policy/outpatient_department/display', area_policy_controller.outpatient_department_display),
    path('admin/area_policy/outpatient_department/add', area_policy_controller.outpatient_department_add),
    path('admin/area_policy/outpatient_department/edit/<int:out_depart_id>',
         area_policy_controller.outpatient_department_edit),
    path('admin/area_policy/outpatient_department/update', area_policy_controller.outpatient_department_update),


    path('admin/user/display', user_controller.display),
    path('admin/user/add', user_controller.add),
    path('admin/user/edit/<int:user_id>', user_controller.edit),
    path('admin/user/update', user_controller.update),


    path('admin/health_report/display', user_controller.health_report_display),

]
