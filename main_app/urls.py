from django.urls import path,include
from . import views
urlpatterns=[
    path("",views.login_view,name="login"),
    path("register/",views.register,name="register"),
    path("dashboard/",views.dashboard_home,name="dashboard"),
    path("cheque/",views.cheque_home,name="cheque"),
    path('cheque/delete/<int:id>/', views.cheque_delete, name='cheque_delete'),
    path("deposit/delete/<int:id>",views.deposit_delete,name='deposit_delete'),
    path('cheque/edit/<int:id>/', views.cheque_edit, name='cheque_edit'),
    path('deposit/submit/',  views.deposit_form, name='deposit_form'),
    path("changepassword/",views.change_password,name="change_password"),

    path("deposit/",views.deposit_home,name="deposit"),
    path("help/",views.help_home,name="help"),
    path("report/",views.report_home,name="report"),
    path("setting/",views.setting_home,name="setting"),
    path("logout/",views.logout_view,name="logout"),
    path("support/",views.login_support,name="support"),
    path("userdelete/<int:id>/",views.delete_user,name="deleteuser"),
    path("datadelete/",views.data_delete,name="datadelete"),
   

    
]