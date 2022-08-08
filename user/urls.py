from django.urls import path
from user.views.UserController import UserController
from user.views.EpidemicSituationController import EpidemicSituationController
from user.views.CaseController import CaseController
from user.views.VaccinesController import VaccinesController
from user.views.AreaPolicyController import AreaPolicyController

user_controller = UserController()
epidemic_situation_controller = EpidemicSituationController()
case_controller = CaseController()
vaccines_controller = VaccinesController()
area_policy_controller = AreaPolicyController()
urlpatterns = [
    path('', user_controller.index),
    path('login', user_controller.login),
    path('register', user_controller.register),
    path('logout', user_controller.logout),
    path('health_report/upload', user_controller.upload_health_report),
    path('vaccines/self', user_controller.self_vaccines_display),
    path('user', user_controller.user),

    path('es', epidemic_situation_controller.display),
    path('case', case_controller.display),
    path('vaccines', vaccines_controller.display),

    path('vaccines/make/<int:vaccines_id>', vaccines_controller.make_vaccines),

    path('outpatient_department', area_policy_controller.outpatient_department_display),
    path('area_policy', area_policy_controller.display)
]