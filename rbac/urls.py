"""TCSDB re_path Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a re_path to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a re_path to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a re_path to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^users_list', views.users_list),
    re_path(r'^users_add', views.users_add),
    re_path(r'^users_del', views.users_del),
    re_path(r'^users_edit', views.users_edit),
    re_path(r'^users_pwd', views.users_pwd),
    re_path(r'^roles_list', views.roles_list),
    re_path(r'^roles_add', views.roles_add),
    re_path(r'^roles_del', views.roles_del),
    re_path(r'^roles_edit', views.roles_edit),
    re_path(r'^permissions_list', views.permissions_list),
    re_path(r'^permissions_add', views.permissions_add),
    re_path(r'^permissions_del', views.permissions_del),
    re_path(r'^permissions_edit', views.permissions_edit),
    re_path(r'^business_list', views.business_list),
    re_path(r'^business_add', views.business_add),
    re_path(r'^business_del', views.business_del),
    re_path(r'^business_edit', views.business_edit),
]
