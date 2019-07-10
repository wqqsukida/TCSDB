from django.test import TestCase
from django.test import Client
from result.api import *
import time
import hashlib
from result.models import *
from cccs.models import *

class ApiTest(TestCase):

    @property
    def auth_header_val(self):
        ctime = str(time.time())
        new_key = "%s|%s" % (settings.API_TOKEN, ctime,)  # asdfuasodijfoausfnasdf|时间戳
        hs = hashlib.md5()
        hs.update(new_key.encode('utf-8'))
        md5_str = hs.hexdigest()
        auth_header_val = "%s|%s" % (md5_str, ctime,)  # 6f800b6a11d3f9c08c77ef8f77b2d460|时间戳
        return auth_header_val

    def setUp(self):
        self.c = Client(HTTP_AUTH_TOKEN=self.auth_header_val)
        cycle_obj2 = TestCycle.objects.create(CycleName='cyclename02', Project='Project02', CycleLevel="SMK")
        plan_obj2_1 = TestPlan.objects.create(CycleID=cycle_obj2,CaseName='TCName01',LoopCnt=2)
        tr_obj_2 = TestRun.objects.create(TCID=cycle_obj2,TestRunName='TRName02',TriggerTime=datetime.datetime.now(),
                                        JIRAID='JIRAID01')

        # cycle_obj1 = TestCycle.objects.create(CycleName='cyclename01',Project='Project01',CycleLevel="SMK")
        # plan_obj1 = TestPlan.objects.create(CycleID=cycle_obj1,CaseName='TCName01',LoopCnt=2)
        # plan_obj2 = TestPlan.objects.create(CycleID=cycle_obj1,CaseName='TCName02',LoopCnt=2)
        # plan_obj3 = TestPlan.objects.create(CycleID=cycle_obj1,CaseName='TCName03',LoopCnt=2)
        # plan_obj4 = TestPlan.objects.create(CycleID=cycle_obj1,CaseName='TCName04',LoopCnt=2)
        # tr_obj = TestRun.objects.create(TCID=cycle_obj1,TestRunName='TRName01',TriggerTime=datetime.datetime.now(),
        #                                 JIRAID='JIRAID01')
        rs_obj = ResultSummary.objects.create(TRName='TRName01',SrtLogRoot='SrtLogRoot01',FWLogRoot='FWLogRoot01',
                                              TotalCases=4,NotRunCnt=4)
        rd_obj1 = ResultDetail.objects.create(TRID=rs_obj,TCName="TCName01",Result="NotRun")
        rd_obj2 = ResultDetail.objects.create(TRID=rs_obj,TCName="TCName02",Result="NotRun")
        rd_obj3 = ResultDetail.objects.create(TRID=rs_obj,TCName="TCName03",Result="NotRun")
        rd_obj4 = ResultDetail.objects.create(TRID=rs_obj,TCName="TCName04",Result="NotRun")
        rd_obj5 = ResultDetail.objects.create(TRID=rs_obj,TCName="TCName05",Result="FAIL")

    def testAddCycleResults(self):
        data = {
            "data":{
                "TRName": "TRName02",
                "SrtLogRoot": "SrtLogRoot02",
                "FWLogRoot": "FWLogRoot02"
            }
        }
        rep = self.c.post(path='/result/api/func/add_res/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddCaseResult(self):
        data = {
            "data":{
                "TRName": "TRName01",
                "TCName": "TCName01",
                "Result": "PASS",
                "StartTime": "2019-07-07 14:51:57",
                "EndTime": "2019-07-09 14:51:57",
                "SerialNum": "SerialNum01",
                "ScriptLog": "ScriptLog01",
                "FWLog": "FWLog01",
            }
        }
        rep = self.c.post(path='/result/api/func/add_case_res/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddCaseDbgInfo(self):
        data = {
            "data":{
                "ResultRecordID": 4,
                "JIRAID": "JIRAID01",
                "FailureKept": True,
                "DebugLog": "DebugLog01",
                "DbgInfo1": "DbgInfo1_1",
                "DbgInfo2": "DbgInfo2_1",
            }
        }
        rep = self.c.post(path='/result/api/func/add_case_dbginfo/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetTestSummary(self):
        data = {
            "data":{
                "TRName":"TRName01"
            }
        }
        rep = self.c.post(path='/result/api/func/get_sum/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetTestLogPath(self):
        data = {
            "data":{
                "TRName":"TRName01"
            }
        }
        rep = self.c.post(path='/result/api/func/get_logroot/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetTestResultDetail(self):
        data = {
            "data":{
                "TRName":"TRName01"
            }
        }
        rep = self.c.post(path='/result/api/func/get_ress/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetTestFailDetail(self):
        data = {
            "data":{
                "TRName":"TRName01"
            }
        }
        rep = self.c.post(path='/result/api/func/get_fail_ress/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)