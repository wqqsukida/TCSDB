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
from result import views
from result import api

urlpatterns = [
    re_path(r'^api/func/add_res/$', api.AddCycleResults.as_view()),
    re_path(r'^api/func/add_case_res/$', api.AddCaseResult.as_view()),
    re_path(r'^api/func/add_case_dbginfo/$', api.AddCaseDbgInfo.as_view()),
    re_path(r'^api/func/get_sum/$', api.GetTestSummary.as_view()),
    re_path(r'^api/func/get_logroot/$', api.GetTestLogPath.as_view()),
    re_path(r'^api/func/get_ress/$', api.GetTestResultDetail.as_view()),
    re_path(r'^api/func/get_fail_ress/$', api.GetTestFailDetail.as_view()),
]
