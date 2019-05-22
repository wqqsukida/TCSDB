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
from . import api
# app_name = 'testcase'

urlpatterns = [
    re_path(r'^api/func_test/add_refspec/$',api.AddRefSpec.as_view()),

    re_path(r'^api/perf_test/add_item/$',api.AddPerfTestItem.as_view()),

    re_path(r'^api/comp_test/add_item/$',api.AddToolTestItem.as_view()),
    re_path(r'^add_project/(\w+)/$', views.AddProject),
    re_path(r'^test_project/(\w+)/$', views.GetProject),
    re_path(r'^edit_project/(\w+)/$', views.UpdateProject),
    re_path(r'^test_cases', views.GetTestCase),
    re_path(r'^add_case', views.AddTestCase),
    re_path(r'^edit_case', views.UpdateTestCase),
    re_path(r'^del_case', views.DeleteTestCase),
    re_path(r'^test_steps', views.GetTestStep),
    re_path(r'^test_specs', views.GetRefSpec),
    re_path(r'^add_spec', views.AddRefSpec),
    re_path(r'^edit_spec', views.UpdateRefSpec),
    re_path(r'^del_spec', views.DeleteRefSpec),
    re_path(r'^test_points', views.GetTestPoint),
    re_path(r'^add_point', views.AddTestPoint),
    re_path(r'^edit_point', views.UpdateTestPoint),
    re_path(r'^del_point', views.DeleteTestPoint),
]
