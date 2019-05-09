# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 5/8/19 2:41 PM
# FileName: api.py
from django.utils.decorators import method_decorator
from django.views import View
from utils.auth_token import api_auth
from django.shortcuts import HttpResponse
import json
from monitor.models import *

class AddDUTNodes(View):
    '''
    增加一个DUT信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeDUTFW(View):
    '''
    更新DUT FW信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeDUTHost(View):
    '''
    更新DUT Host信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class AddDUTMonitorRec(View):
    '''
    增加一次DUT健康监控记录
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class GetDUTBasicInfo(View):
    '''
    获得DUT基本信息（包含FW版本和Host信息）
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetDUTHealthInfo(View):
    '''
    获得DUT健康信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetAllDUTByHostName(View):
    '''
    获得主机上所有DUT的SN
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetAllDUTByGroupID(View):
    '''
    获得同组的所有DUT的SN
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetAllDUTByTag(View):
    '''
    获得相同标签的所有DUT的SN
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class FindDuts(View):
    '''
    查询所有符合条件的DUT的SN
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class ChangeDUTGroupID(View):
    '''
    更新DUT的GroupID信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeDUTTags(View):
    '''
    更新DUT的Tag信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeDUTStatus(View):
    '''
    更新DUT的状态
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class GetDUTStatus(View):
    '''
    获得DUT的状态
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetDUTTags(View):
    '''
    获得DUT的Tags
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetDUTGroupID(View):
    '''
    获得DUT的GroupID
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

########################################################################################################################
class AddHostInfo(View):
    '''
    新增Host机器信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeHostHWInfo(View):
    '''
    更新Host机器硬件配置信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeHostNetInfo(View):
    '''
    更新Host机器网络配置信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeSlotDUTInfo(View):
    '''
    新增/更新Slot上DUT的信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeHostOSInfo(View):
    '''
    更新Host机器OS信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeHostDriverInfo(View):
    '''
    新增/更新Host机器驱动信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class AddHostMonitorRec(View):
    '''
    新增一条Host机器的健康状态监控记录
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class ChangeHostSWInfo(View):
    '''
    新增/更新Host机器上测试软件安装信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))

class GetHostBasicInfo(View):
    '''
    获得Host机器的基本信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetHostHWInfo(View):
    '''
    获得Host机器的硬件信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetHostNetInfo(View):
    '''
    获得Host机器的网络配置信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetHostOSInfo(View):
    '''
    获得Host机器的OS信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetHostDriverInfo(View):
    '''
    获得Host机器的驱动信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetHostToolsInfo(View):
    '''
    获得Host机器的工具版本信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetHostCurStatus(View):
    '''
    获得Host机器当前的硬件使用状态
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetAllSlotsByHostName(View):
    '''
    获得Host机器上所有Slot的信息
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class FindHosts(View):
    '''
    获得符合条件的Host机器列表
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))

class GetDisconnectedHost(View):
    '''
    获得掉线的Host机器清单
    '''
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}
        return HttpResponse(json.dumps(response))

    @method_decorator(api_auth)
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'only get method!'}
        return HttpResponse(json.dumps(response))