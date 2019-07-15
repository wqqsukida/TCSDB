# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 7/3/19 5:41 PM
# FileName: api.py
from utils.auth_token import APIAuthView,APITokenAuthView
from django.shortcuts import HttpResponse
from django.db import transaction
import json,traceback
import datetime
from result.models import *
from cccs.models import *
from django.db.models import Max
from django.conf import settings

TEST = settings.TESTING

class AddCycleResults(APIAuthView):
    '''
    新增功能测试结果信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            srt_log = res.get("SrtLogRoot")
            fw_log = res.get("FWLogRoot")
            tr_obj = TestRun.objects.get(TestRunName=tr_name)
            total_cases = tr_obj.TCID.testplan_set.count()
            with transaction.atomic():
                res_sum = ResultSummary.objects.create(TRName=tr_name,TotalCases=total_cases,
                                             NotRunCnt=total_cases,SrtLogRoot=srt_log,
                                             FWLogRoot=fw_log)
                for tp in tr_obj.TCID.testplan_set.all():
                    ResultDetail.objects.create(TRID=res_sum,TCName=tp.CaseName,Result='NotRun')

            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class AddCaseResult(APIAuthView):
    '''
    新增功能测试用例结果信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            tc_name = res.get("TCName")
            result = res.get("Result")
            start = res.get("StartTime")
            end = res.get("EndTime")
            sn = res.get("SerialNum")
            srt_log = res.get("ScriptLog")
            fw_log = res.get("FWLog")

            rs_obj = ResultSummary.objects.get(TRName=tr_name)
            with transaction.atomic():
                rd_obj = ResultDetail.objects.filter(TRID=rs_obj,TCName=tc_name)
                rd_obj.update(Result=result,StartTime=start,EndTime=end,SerialNum=sn,
                              ScriptLog=srt_log,FWLog=fw_log)
                rs_obj.NotRunCnt -= 1
                if result == 'PASS':
                    rs_obj.PassCnt += 1
                elif result == 'CPASS':
                    rs_obj.CPassCnt += 1
                elif result == 'FAIL':
                    rs_obj.FailCnt += 1
                elif result == 'ABORT':
                    rs_obj.AbortCnt += 1
                elif result == 'SKIP':
                    rs_obj.SkipCnt += 1
                rs_obj.save()

            response = {'code':0,'msg':'Success!','data':{'ResultRecordID':rd_obj.first().id}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))


class AddCaseDbgInfo(APIAuthView):
    '''
    新增功能测试调试信息记录
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            rr_id = res.get("ResultRecordID")
            jira_id = res.get("JIRAID")
            failure_kept = res.get("FailureKept")
            debug_log = res.get("DebugLog")
            dbg_info1 = res.get("DbgInfo1")
            dbg_info2 = res.get("DbgInfo2")

            rd_obj = ResultDetail.objects.filter(id=rr_id)
            ResultFailure.objects.create(RRID=rd_obj.first(),JIRAID=jira_id,FailureKept=failure_kept,
                                         DebugLog=debug_log,DbgInfo1=dbg_info1,DbgInfo2=dbg_info2)

            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetTestSummary(APIAuthView):
    '''
    获得功能测试结果统计信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            rs_obj = ResultSummary.objects.filter(TRName=tr_name)
            data = rs_obj.values('TRName','TotalCases','PassCnt','FailCnt','AbortCnt',
                                 'SkipCnt','CPassCnt','NotRunCnt').first()
            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetTestLogPath(APIAuthView):
    '''
    获得测试的Log路径
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            rs_obj = ResultSummary.objects.filter(TRName=tr_name)
            data = rs_obj.values('SrtLogRoot','FWLogRoot').first()
            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetTestResultDetail(APIAuthView):
    '''
    获得详细功能测试结果信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            rs_obj = ResultSummary.objects.get(TRName=tr_name)
            query_set = rs_obj.resultdetail_set.all()
            data = []
            for q in query_set:
                q_dict = {"TCName":q.TCName,"Result":q.Result,"SerialNum":q.SerialNum,
                          "ScriptLog":q.ScriptLog,"FWLog":q.FWLog}
                if q.StartTime:q_dict["StartTime"] = q.StartTime.strftime('%Y-%m-%d %H:%m:%s')
                if q.EndTime:q_dict["EndTime"] = q.EndTime.strftime('%Y-%m-%d %H:%m:%s')
                data.append(q_dict)
            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetTestFailDetail(APIAuthView):
    '''
    获得FAIL功能测试调试信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            rd_objs = ResultSummary.objects.get(TRName=tr_name).resultdetail_set.all()
            data = []
            for rd in rd_objs:
                rf_obj = rd.resultfailure_set.first()
                if rf_obj:
                    data_dic = {"TCName":rd.TCName,"JIRAID":rf_obj.JIRAID,"FailureKept":rf_obj.FailureKept,
                                "DebugLog":rf_obj.DebugLog,"DbgInfo1":rf_obj.DbgInfo1,"DbgInfo2":rf_obj.DbgInfo2}
                    data.append(data_dic)
            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

############################################################################################################

class AddCycleTestResult(APIAuthView):
    '''
    新增性能测试结果
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            log_root = res.get("LogRoot")
            tr_obj = TestRun.objects.get(TestRunName=tr_name)
            total_cases = tr_obj.TCID.testplan_set.count()
            with transaction.atomic():
                res_sum = PerfResultSummary.objects.create(TRName=tr_name,TotalCases=total_cases,
                                             LogRoot=log_root)
                for tp in tr_obj.TCID.testplan_set.all():
                    pd_obj = PerfResultDetail.objects.create(TRID=res_sum,TCName=tp.CaseName)
                    PerfResultItem.objects.create(RRID=pd_obj)
            response = {'code':0,'msg':'Success!','data':{"TestResultID":res_sum.id}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChgCaseRecord(APIAuthView):
    '''
    更新测试结果具体信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_id = res.get("TRID")
            tc_name = res.get("TCName")
            start = res.get("StartTime")
            end = res.get("EndTime")
            sn = res.get("SerialNum")
            srt_log = res.get("ScriptLog")
            fw_log = res.get("FWLog")
            stat_log = res.get("StatLog")

            rs_obj = PerfResultSummary.objects.get(id=tr_id)
            with transaction.atomic():
                rd_obj = PerfResultDetail.objects.filter(TRID=rs_obj,TCName=tc_name)
                rd_obj.update(StartTime=start,EndTime=end,SerialNum=sn,
                              ScriptLog=srt_log,FWLog=fw_log,StatLog=stat_log)
                rs_obj.RunCases += 1
                rs_obj.save()

            response = {'code':0,'msg':'Success!','data':{"ResultRecordID":rd_obj.first().id}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChgItemRecord(APIAuthView):
    '''
    更新测试项具体结果信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            rr_id = res.get("RRID")
            item_name = res.get("ItemName")
            unit = res.get("Unit")
            value = res.get("Value")
            raw_data = res.get("RawData")

            rd_obj = PerfResultDetail.objects.get(id=rr_id)
            with transaction.atomic():
                ri_obj = PerfResultItem.objects.filter(RRID=rd_obj)
                ri_obj.update(ItemName=item_name,Unit=unit,Value=value,RawData=raw_data)

                rd_obj.TRID.RunItems += 1
                rd_obj.TRID.save()

            response = {'code':0,'msg':'Success!','data':{"ResultItemID":ri_obj.first().id}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetRsltSummary(APIAuthView):
    '''
    获得测试结果统计信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            rs_obj = PerfResultSummary.objects.filter(TRName=tr_name)
            data = rs_obj.values('TotalCases','TotalItems','RunCases','RunItems',
                                 'LogRoot').first()
            data["TestResultID"] = rs_obj.first().id

            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetCaseRsltInfo(APIAuthView):
    '''
    获得测试结果用例相关信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            tc_name = res.get("TCName")
            rd_obj = PerfResultDetail.objects.get(TCName=tc_name,TRID__TRName=tr_name)
            data = {"SerialNum":rd_obj.SerialNum,"ScriptLog":rd_obj.ScriptLog,
                    "FWLog":rd_obj.FWLog,"StatLog":rd_obj.StatLog}
            if rd_obj.StartTime:data["StartTime"] = rd_obj.StartTime.strftime('%Y-%m-%d %H:%m:%s')
            if rd_obj.EndTime:data["EndTime"] = rd_obj.EndTime.strftime('%Y-%m-%d %H:%m:%s')

            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetTestRunCases(APIAuthView):
    '''
    获得该轮测试所有的测试用例
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            tp_objs = TestRun.objects.get(TestRunName=tr_name).TCID.testplan_set.all()
            data = [tp.CaseName for tp in tp_objs]
            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetTestRunItems(APIAuthView):
    '''
    获得该轮测试用例对应的测试项列表
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.  decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            tc_name = res.get("TCName")
            rd_obj = PerfResultDetail.objects.get(TRID__TRName=tr_name,TCName=tc_name)
            data = [item.ItemName for item in rd_obj.perfresultitem_set.all()]
            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetItemResult(APIAuthView):
    '''
    获得该轮测试项的测试结果信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tr_name = res.get("TRName")
            tc_name = res.get("TCName")
            item_name = res.get("ItemName")
            ri_obj = PerfResultItem.objects.filter(RRID__TCName=tc_name,RRID__TRID__TRName=tr_name,
                                                   ItemName=item_name)
            data = ri_obj.values("Unit","Value","RawData").first()
            response = {'code':0,'msg':'Success!','data':data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))