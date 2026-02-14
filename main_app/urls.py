from django.urls import path,include
from . import views
urlpatterns=[
    path("",views.login_view,name="login"),
    path("register/",views.register,name="register"),
    path("dashboard/",views.dashboard_home,name="dashboard"),
    path("cheque/",views.cheque_home,name="cheque"),
    path("deposit/",views.deposit_home,name="deposit"),
    path("help/",views.help_home,name="help"),
    path("report/",views.report_home,name="report"),
    path("setting/",views.setting_home,name="setting"),
]