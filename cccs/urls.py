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
from cccs import views
from cccs import api

urlpatterns = [
    re_path(r'^api/add_cycle/$', api.AddTestCycle.as_view()),
    re_path(r'^api/add_plan/$', api.AddCaseIntoPlan.as_view()),
    re_path(r'^api/add_run/$', api.AddTestRun.as_view()),
    re_path(r'^api/start_run/$', api.StartTestRun.as_view()),
    re_path(r'^api/stop_run/$', api.StopTestRun.as_view()),
    re_path(r'^api/get_cycle/$', api.GetTestCycle.as_view()),
    re_path(r'^api/get_cases/$', api.GetCycleCaseList.as_view()),
    re_path(r'^api/get_run/$', api.GetTestRunInfo.as_view()),
    re_path(r'^api/find_cycle/$', api.FindTestCycle.as_view()),
    re_path(r'^api/find_run/$', api.FindTestRun.as_view()),
    re_path(r'^api/add_comment/$', api.AddTRComments.as_view()),
    re_path(r'^api/change_cyc_status/$', api.ChgCycleStatus.as_view()),
    re_path(r'^api/change_plc_status/$', api.ChgPlanCaseStatus.as_view()),

    re_path(r'^test_cycles$', views.test_cycles),
    re_path(r'^test_cycles/add/$', views.add_test_cycle),
    re_path(r'^test_cycles/update/$', views.update_test_cycle),
    re_path(r'^test_plans/(?P<tc_id>\d*)/$', views.test_plans),
    re_path(r'^test_plans/add/$', views.add_test_plan),
    re_path(r'^test_plans/update/$', views.update_test_plan),
    re_path(r'^run_records/(?P<tc_id>\d*)/(?P<t_status>\w*)/', views.run_records),
    re_path(r'^test_run/add/$', views.add_test_run),
    re_path(r'^test_run/update/$', views.update_test_run),
    re_path(r'^test_run/del/$', views.del_test_run),
    re_path(r'^test_actions/(?P<tc_id>\d*)/(?P<tp_id>\d*)/', views.actions),
]
