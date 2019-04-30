# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 4/29/19 9:20 AM
# FileName: views.py

from django.shortcuts import render,redirect,HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.http import FileResponse
from rbac.models import *
from rbac.service.init_permission import init_permission
import copy
import json
import random
import datetime
import os
from utils.md5 import encrypt
from django.forms import Form,fields,widgets
# from .models import *
from django.db.models import Q
from django.urls import reverse
from utils.pagination import Pagination
from django.http.request import QueryDict
from django.conf import settings
from utils.filter_row import Row
from django.forms.models import model_to_dict
from utils.log import logger
#========================================================================#
def init_paginaion(request,queryset):
    # 初始化分页器
    query_params = copy.deepcopy(request.GET)  # QueryDict
    current_page = request.GET.get('page', 1)
    # per_page = config.per_page
    # pager_page_count = config.pager_page_count
    all_count = queryset.count()
    base_url = request.path_info
    page_obj = Pagination(current_page, all_count, base_url, query_params)
    query_set = queryset[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()

    return query_set,page_html
#========================================================================#
class LoginForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={'required':'*用户名不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control uname',
                                        'type':'text',
                                        'id':'inputUsername3',
                                        'placeholder':'用户名',
                                        'name':'username'
                                        })
    )
    password = fields.CharField(
        required=True,
        error_messages={'required': '*密码不能为空'},
        widget = widgets.PasswordInput(attrs={'class':'form-control pword m-b',
                                        'id':'inputPassword3',
                                        'placeholder':'密码',
                                        'name':'password'
                                        })
    )

    code = fields.CharField(
        required=True,
        error_messages={'required': '*验证码不能为空'},
        widget = widgets.TextInput(attrs={'class':'form-control',
                                        'id':'inputCode',
                                        'placeholder':'验证码',
                                        'name':'code',
                                        'style':'width:55%;display:inline-block'
                                        }),

    )
#========================================================================#
def login(request):
    '''
    login登录验证函数
    '''
    if request.method == "GET":
        form = LoginForm()
        return render(request,'login_v2.html',{'form':form})
    else:
        response = {'status': True, 'data': None, 'msg': None}
        form = LoginForm(request.POST)
        if form.is_valid():
            user = request.POST.get('username',None)  #获取input标签里的username的值 None：获取不到不会报错
            pwd = request.POST.get('password',None)
            code = request.POST.get('code',None)
            # print(code,request.session['keep_valid_code'])

            if  code.lower() == request.session['keep_valid_code'].lower(): #比对验证码

                pwd = encrypt(pwd) #md5加密密码字符串
                user_obj = AdminInfo.objects.filter(username=user, password=pwd).first()

                if user_obj:
                    role = user_obj.user.roles.values('title')
                    # print(role)
                    if role:
                        role = role.first().get('title')
                    else:
                        role = '访客'
                    request.session['is_login'] = {'user': user_obj.user.name, 'role': role}  # 仅作为登录后用户名和身份显示session
                    init_permission(user_obj, request)
                    response['data'] = {}
                    logger.info('user [{0}] login success.'.format(user_obj.user.name))
                else:
                    response['status'] = False
                    response['msg'] = {'password': ['*用户名或者密码错误']}
            else:
                response['status'] = False
                response['msg'] = {'code': ['*请填写正确的验证码']}
        else:
            response['status'] = False
            response['msg'] = form.errors
        # print(response)
        return HttpResponse(json.dumps(response))

def logout(request):
    '''
    logout删除session函数
    '''
    user = request.session.get("is_login")
    if user:
        logger.info('user [{0}] logout.'.format(user['user']))
    request.session.clear() #删除session
    return HttpResponseRedirect('/login/')

def forbidden(request):
    return render(request,'403.html')

def page_not_found(request,exception):
    return render(request,'404.html')

def index(request):
    '''
    index页面函数
    '''
    user_dict = request.session.get('is_login', None)
    username = user_dict['user']
    user_obj = UserProfile.objects.get(name=username)
    user_role = user_dict['role']
    # print('---当前登录用户/角色--->',username,user_role)
    return render(request,'index.html',locals())


def index_v3(request):
    '''
    首页
    :param request:
    :return:
    '''
    if request.method == "GET":

        return render(request,'index_v3.html',locals())