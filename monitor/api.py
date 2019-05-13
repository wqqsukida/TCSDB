# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 5/8/19 2:41 PM
# FileName: api.py
from django.utils.decorators import method_decorator
from utils.auth_token import APIAuthView
from django.shortcuts import HttpResponse
import json
from monitor.models import *

class AddDUTNodes(APIAuthView):
    '''
    增加一个DUT信息
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

class ChangeDUTFW(APIAuthView):
    '''
    更新DUT FW信息
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

class ChangeDUTHost(APIAuthView):
    '''
    更新DUT Host信息
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

class AddDUTMonitorRec(APIAuthView):
    '''
    增加一次DUT健康监控记录
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

class GetDUTBasicInfo(APIAuthView):
    '''
    获得DUT基本信息（包含FW版本和Host信息）
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetDUTHealthInfo(APIAuthView):
    '''
    获得DUT健康信息
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetAllDUTByHostName(APIAuthView):
    '''
    获得主机上所有DUT的SN
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetAllDUTByGroupID(APIAuthView):
    '''
    获得同组的所有DUT的SN
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetAllDUTByTag(APIAuthView):
    '''
    获得相同标签的所有DUT的SN
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class FindDuts(APIAuthView):
    '''
    查询所有符合条件的DUT的SN
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class ChangeDUTGroupID(APIAuthView):
    '''
    更新DUT的GroupID信息
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

class ChangeDUTTags(APIAuthView):
    '''
    更新DUT的Tag信息
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

class ChangeDUTStatus(APIAuthView):
    '''
    更新DUT的状态
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

class GetDUTStatus(APIAuthView):
    '''
    获得DUT的状态
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetDUTTags(APIAuthView):
    '''
    获得DUT的Tags
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetDUTGroupID(APIAuthView):
    '''
    获得DUT的GroupID
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

########################################################################################################################
class AddHostInfo(APIAuthView):
    '''
    新增Host机器信息
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

class ChangeHostHWInfo(APIAuthView):
    '''
    更新Host机器硬件配置信息
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

class ChangeHostNetInfo(APIAuthView):
    '''
    更新Host机器网络配置信息
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

class ChangeSlotDUTInfo(APIAuthView):
    '''
    新增/更新Slot上DUT的信息
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

class ChangeHostOSInfo(APIAuthView):
    '''
    更新Host机器OS信息
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

class ChangeHostDriverInfo(APIAuthView):
    '''
    新增/更新Host机器驱动信息
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

class AddHostMonitorRec(APIAuthView):
    '''
    新增一条Host机器的健康状态监控记录
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

class ChangeHostSWInfo(APIAuthView):
    '''
    新增/更新Host机器上测试软件安装信息
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

class GetHostBasicInfo(APIAuthView):
    '''
    获得Host机器的基本信息
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetHostHWInfo(APIAuthView):
    '''
    获得Host机器的硬件信息
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetHostNetInfo(APIAuthView):
    '''
    获得Host机器的网络配置信息
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetHostOSInfo(APIAuthView):
    '''
    获得Host机器的OS信息
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetHostDriverInfo(APIAuthView):
    '''
    获得Host机器的驱动信息
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetHostToolsInfo(APIAuthView):
    '''
    获得Host机器的工具版本信息
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetHostCurStatus(APIAuthView):
    '''
    获得Host机器当前的硬件使用状态
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetAllSlotsByHostName(APIAuthView):
    '''
    获得Host机器上所有Slot的信息
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class FindHosts(APIAuthView):
    '''
    获得符合条件的Host机器列表
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))

class GetDisconnectedHost(APIAuthView):
    '''
    获得掉线的Host机器清单
    '''
    
    def get(self,request,*args,**kwargs):
        print(request.GET)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}
        return HttpResponse(json.dumps(response))

    
    def post(self,request,*args,**kwargs):
        response = {'code': 1, 'msg': 'Request method error!'}
        return HttpResponse(json.dumps(response))