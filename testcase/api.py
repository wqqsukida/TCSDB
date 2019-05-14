# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 5/13/19 3:03 PM
# FileName: api.py
from django.shortcuts import render,HttpResponse
from utils.auth_token import APIAuthView
import json
from testcase.models import *

class AddRefSpec(APIAuthView):
    '''
    新增参考文档信息
    '''
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'Request method error!'}
        return HttpResponse(json.dumps(response))

    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}

        return HttpResponse(json.dumps(response))

class AddPerfTestItem(APIAuthView):
    '''
    新增性能测试项
    '''
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'Request method error!'}
        return HttpResponse(json.dumps(response))

    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}

        return HttpResponse(json.dumps(response))

class AddToolTestItem(APIAuthView):
    '''
    新增兼容性测试项
    '''
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'Request method error!'}
        return HttpResponse(json.dumps(response))

    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}

        return HttpResponse(json.dumps(response))
