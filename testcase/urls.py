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
    #automated function api
    re_path(r'^api/func_test/add_refspec/$',api.AddRefSpec.as_view()),
    re_path(r'^api/func_test/add_testpoint/$',api.AddTestPoint.as_view()),
    re_path(r'^api/func_test/add_testcase/$',api.AddCaseDesc.as_view()),
    re_path(r'^api/func_test/mod_casestep/$',api.UpdateCaseStep.as_view()),
    re_path(r'^api/func_test/mod_caseversion/$',api.UpdateCaseVersion.as_view()),
    re_path(r'^api/func_test/mod_casestrinfo/$',api.UpdateCaseSrtInfo.as_view()),
    re_path(r'^api/func_test/mod_caseowner/$',api.UpdateCaseOwnership.as_view()),
    re_path(r'^api/func_test/mod_caseproject/$',api.UpdateCaseProject.as_view()),
    re_path(r'^api/func_test/mod_casecategory/$',api.UpdateCaseCategory.as_view()),
    re_path(r'^api/func_test/mod_caselabel/$',api.UpdateCaseLabels.as_view()),
    re_path(r'^api/func_test/mod_casedepinfo/$',api.UpdateCaseDepInfo.as_view()),
    re_path(r'^api/func_test/get_casescript/$',api.GetCaseScriptInfo.as_view()),
    re_path(r'^api/func_test/get_caseowner/$',api.GetCaseSrtOwner.as_view()),
    re_path(r'^api/func_test/get_casedetail/$',api.GetCaseDetailedInfo.as_view()),
    re_path(r'^api/func_test/get_casestep/$',api.GetCaseStepInfo.as_view()),
    re_path(r'^api/func_test/get_casepoint/$',api.GetCaseTestPoints.as_view()),
    re_path(r'^api/func_test/get_caseprjinfo/$',api.GetCaseProjectInfo.as_view()),
    re_path(r'^api/func_test/get_prjcaselist/$',api.GetProjectCases.as_view()),
    #automated performance api
    re_path(r'^api/perf_test/add_testcase/$',api.AddCaseDesc.as_view()),
    #automated competible api
    re_path(r'^api/comp_test/add_item/$',api.AddToolTestItem.as_view()),
    #function web api
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
