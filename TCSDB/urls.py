"""TCSDB path Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a path to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import re_path,include
from TCSDB import views
from utils import get_code_img
from utils.auth_token import LoginAuth
urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^rbac/',include('rbac.urls')),
    re_path(r'^monitor/',include('monitor.urls')),
    re_path(r'^testcase/',include('testcase.urls')),
    re_path(r'^cccs/',include('cccs.urls')),
    re_path(r'^api/auth/', LoginAuth.as_view()),
    re_path(r'^login/', views.login),
    re_path(r'^get_code/', get_code_img.get_code),
    re_path(r'^logout/', views.logout),
    re_path(r'^index/', views.index),
    re_path(r'^index_v3/', views.index_v3),
    re_path(r'^403/', views.forbidden),
    re_path(r'^$', views.index),
]

handler404 = 'TCSDB.views.page_not_found'