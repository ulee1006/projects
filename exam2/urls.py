from django.contrib import admin
from django.urls import path
from examapp import views

urlpatterns = [
    path('',views.main),
    path('processreg', views.procregister),
    path('dashboard',views.dashboard),
    path('processlogin', views.validate_login),
    path('main', views.index),
    path('logout', views.logout),
    path('add_plan', views.add_plan),
    path('create_plan', views.create_plan),
    path('show_plan/<id>', views.show_plan),
    path('join_plan/<plan_id>', views.join_plan),
    
]




