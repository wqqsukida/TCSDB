"""TCSDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^api/list/$', views.ApiList.as_view()),
    re_path(r'^test_cases', views.test_cases),
    re_path(r'^test_specs', views.GetRefSpec),
    re_path(r'^add_spec', views.AddRefSpec),
    re_path(r'^edit_spec', views.UpdateRefSpec),
    re_path(r'^del_spec', views.DeleteRefSpec),
    re_path(r'^test_points', views.GetTestPoint),
    re_path(r'^add_point', views.AddTestPoint),
    re_path(r'^edit_point', views.UpdateTestPoint),
    re_path(r'^del_point', views.DeleteTestPoint),
    re_path(r'^test_detail_cases', views.test_detail_cases),
    re_path(r'^oc_test_cases', views.oc_test_cases),
    re_path(r'^taiplus_test_cases', views.taiplus_test_cases),
    re_path(r'^oc_perf_test_cases', views.oc_perf_test_cases),
    re_path(r'^taiplus_perf_test_cases', views.taiplus_perf_test_cases),
    re_path(r'^test_perf_detail_cases', views.test_perf_detail_cases),
    re_path(r'^oc_com_test_cases', views.oc_com_test_cases),
    re_path(r'^taiplus_com_test_cases', views.taiplus_com_test_cases),
    re_path(r'^test_com_detail_cases', views.test_com_detail_cases),
]
