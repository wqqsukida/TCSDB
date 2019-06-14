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
            TestRun.objects.create(**res,TCID=cycle_obj.first())
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
        response = {}
        try:
            with transaction.atomic():
                tr_name = res.pop("TestRunName")
                tr_obj = TestRun.objects.filter(TestRunName=tr_name)
                if tr_obj.first().Status=='RUNING':raise Exception('TestRun already running!')
                tr_obj.update(**res,Status='RUNING',StartTime=datetime.datetime.now())
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
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            cycle_name = res.get("CycleName")
            tc_obj = TestCycle.objects.filter(CycleName=cycle_name)
            data = tc_obj.first().testplan_set.filter(Status='ACTIVE').values()
            data = [i.get('CaseName') for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))


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
            if tr_obj.first().StartTime:
                data['StartTime'] = tr_obj.first().StartTime.strftime("%Y-%m-%d %H:%m:%s")
            if tr_obj.first().EndTime:
                data['EndTime'] = tr_obj.first().EndTime.strftime("%Y-%m-%d %H:%m:%s")
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class FindTestCycle(APIAuthView):
    '''
    查询符合条件的TestCycle
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            project = res.get("Project")
            cycle_level = res.get("CycleLevel")
            status = res.get("Status")
            timeDelta = res.get("timeDelta") # 获取天数,查询几天前的数据
            parms_dict = {}
            if project and project != "ALL":
                parms_dict["Project"] = project
            if cycle_level and cycle_level != "ALL":
                parms_dict["HostName"] = cycle_level
            if status and status != "ALL":
                parms_dict["Interface"] = status

            data = TestCycle.objects.filter(**parms_dict).values("CycleName")
            if timeDelta:
                date_time = datetime.datetime.now() - datetime.timedelta(days=timeDelta)
                data.filter(Created__gt=date_time)
            data = [i.get("CycleName") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class FIndTestRun(APIAuthView):
    '''
    查询符合条件的TestRun
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            project = res.get("Project")
            cycle_name = res.get("CycleName")
            cycle_level = res.get("CycleLevel")
            status = res.get("Status")
            jira_id = res.get("JIRAID")
            timeDelta = res.get("timeDelta")
            parms_dict = {}
            if project and project != "ALL":
                parms_dict["Project"] = project
            if cycle_level and cycle_level != "ALL":
                parms_dict["HostName"] = cycle_level
            if status and status != "ALL":
                parms_dict["Interface"] = status

            data = TestCycle.objects.filter(**parms_dict).values("CycleName")
            data = [i.get("CycleName") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class AddTRComments(APIAuthView):
    '''
    新增/更新TestRun的Comments
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TestRunName")
            comments = res.get("Comments")
            tr_obj = TestRun.objects.filter(TestRunName=tr_name)
            tr_obj.update(Comments=comments)
            response = {'code': 0, 'msg': 'Success!', 'data': True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChgCycleStatus(APIAuthView):
    '''
    更新TestCycle状态
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            cycle_name = res.get("CycleName")
            status = res.get("Status")
            operator = 'Test' if TEST else request.session['api_auth'].get("user")
            tc_obj = TestCycle.objects.filter(CycleName = cycle_name)
            TestAction.objects.create(ActionType = 1,
                                      OriginalVal = tc_obj.first().Status,
                                      NewVal = status,
                                      ActionOP = operator,
                                      CycleID = tc_obj.first()
                                      )
            tc_obj.update(Status=status)
            response = {'code': 0, 'msg': 'Success!', 'data': True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChgPlanCaseStatus(APIAuthView):
    '''
    更新Test Cycle里Case的状态
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            cycle_name = res.get("CycleName")
            case_name = res.get("CaseName")
            status = res.get("Status")
            operator = 'Test' if TEST else request.session['api_auth'].get("user")
            tc_obj = TestCycle.objects.filter(CycleName = cycle_name)
            tp_obj = TestPlan.objects.filter(CycleID=tc_obj.first(),CaseName=case_name)
            TestAction.objects.create(ActionType = 2,
                                      OriginalVal = tp_obj.first().Status,
                                      NewVal = status,
                                      ActionOP = operator,
                                      PlanID = tp_obj.first(),
                                      CycleID = tc_obj.first()
                                      )
            tp_obj.update(Status=status)
            response = {'code': 0, 'msg': 'Success!', 'data': True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))