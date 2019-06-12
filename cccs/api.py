# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 6/10/19 9:54 AM
# FileName: api.py
from utils.auth_token import APIAuthView,APITokenAuthView
from django.shortcuts import HttpResponse
from django.db import transaction
import json,traceback
import datetime
from cccs.models import *
from django.db.models import Max
from django.conf import settings

TEST = settings.TESTING

class AddTestCycle(APIAuthView):
    '''
    新增TestCycle
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            TestCycle.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class AddCaseIntoPlan(APIAuthView):
    '''
    新增TestCase到TestPlan
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            cycle_name = res.pop("CycleName")
            cycle_obj = TestCycle.objects.filter(CycleName=cycle_name)
            TestPlan.objects.create(**res,CycleID=cycle_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class AddTestRun(APIAuthView):
    '''
    新增TestRun
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            cycle_name = res.pop("CycleName")
            cycle_obj = TestCycle.objects.filter(CycleName=cycle_name)
            TestRun.objects.create(**res,CycleID=cycle_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class StartTestRun(APIAuthView):
    '''
    开始某个TestRun
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            with transaction.atomic():
                tr_name = res.pop("TestRunName")
                tr_obj = TestRun.objects.filter(TestRunName=tr_name)
                tr_obj.update(**res,Status='RUNING',StratTime=datetime.datetime.now())
                tc_obj = tr_obj.first().TCID
                tc_obj.TriggeredTotal += 1
                tc_obj.LastTriggered = datetime.datetime.now()
                tc_obj.save()
                response = {'code': 0, 'msg': 'Success!', 'data': True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class StopTestRun(APIAuthView):
    '''
    结束某个TestRun
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TestRunName")
            tr_obj = TestRun.objects.filter(TestRunName=tr_name)
            tr_status = res.get("Status")
            tr_obj.update(Status=tr_status,EndTime=datetime.datetime.now())
            response = {'code': 0, 'msg': 'Success!', 'data': True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetTestCycle(APIAuthView):
    '''
    获得TestCycle信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            cycle_name = res.get("CycleName")
            cycle_obj = TestCycle.objects.filter(CycleName=cycle_name)
            data = cycle_obj.values('CycleName', 'Project', 'CycleLevel', 'Status',
                                  'TriggeredTotal').first()
            data['Created'] = cycle_obj.first().Created.strftime("%Y-%m-%d %H:%m:%s")
            data['LastTriggered'] = cycle_obj.first().LastTriggered.strftime("%Y-%m-%d %H:%m:%s")
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetCycleCaseList(APIAuthView):
    '''
    获得TestCycle Script清单
    '''

class GetTestRunInfo(APIAuthView):
    '''
    获得TestRun的信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TestRunName")
            tr_obj = TestRun.objects.filter(TestRunName=tr_name)
            data = tr_obj.values('TestRunName', 'Status', 'TCID', 'JIRAID',
                                  'DUTGRPID','FWPkgName','SrtPkgName').first()
            data['StartTime'] = tr_obj.first().StartTime.strftime("%Y-%m-%d %H:%m:%s")
            data['EndTime'] = tr_obj.first().EndTime.strftime("%Y-%m-%d %H:%m:%s")
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))