from django.test import TestCase
from django.test import Client
from cccs.api import *
import time
import hashlib
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
        cycle_obj = TestCycle.objects.create(CycleName='CycleName01',Project='Project01',CycleLevel="SMK")
        plan_obj = TestPlan.objects.create(CycleID=cycle_obj,CaseName='CaseName01',LoopCnt=2)
        tr_obj = TestRun.objects.create(TCID=cycle_obj,TestRunName='TestRunName01',TriggerTime=datetime.datetime.now(),
                                        JIRAID='JIRAID01')
        plan_obj.Status = 'ACTIVE'
        plan_obj.save()

    def testAddTestCycle(self):
        data = {
            "data":{
                "CycleName": "CycleName02",
                "Project": "Project01",
                "CycleLevel": "DRT"
            }
        }
        rep = self.c.post(path='/cccs/api/add_cycle/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddCaseIntoPlan(self):
        data = {
            "data":{
                "CycleName": "CycleName01",
                "CaseName": "CaseName02",
                "LoopCnt": 2
            }
        }
        rep = self.c.post(path='/cccs/api/add_plan/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddTestRun(self):
        data = {
            "data":{
                "CycleName": "CycleName01",
                "TestRunName": "TestRunName02",
                "TriggerTime": "2019-06-18 10:13:20",
                "JIRAID": "JIRAID01",
            }
        }
        rep = self.c.post(path='/cccs/api/add_run/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testStartTestRun(self):
        data = {
            "data":{
                "TestRunName": "TestRunName01",
                "DUTGRPID": 51,
                "FWPkgName": "FWPkgName01",
                "SrtPkgName": "SrtPkgName01",
            }
        }
        rep = self.c.post(path='/cccs/api/start_run/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testStopTestRun(self):
        data = {
            "data":{
                "TestRunName": "TestRunName01",
                "Status": "FINISHED",
            }
        }
        rep = self.c.post(path='/cccs/api/stop_run/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetTestCycle(self):
        data = {
            "data":{
                "CycleName": "CycleName01",
            }
        }
        rep = self.c.post(path='/cccs/api/get_cycle/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetCycleCaseList(self):
        data = {
            "data":{
                "CycleName": "CycleName01",
            }
        }
        rep = self.c.post(path='/cccs/api/get_cases/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetTestRunInfo(self):
        data = {
            "data":{
                "TestRunName": "TestRunName01",
            }
        }
        rep = self.c.post(path='/cccs/api/get_run/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testFindTestCycle(self):
        data = {
            "data":{
                "Project": "Project01",
                "CycleLevel": "SMK",
                "CreatedTimeDelta":1,
            }
        }
        rep = self.c.post(path='/cccs/api/find_cycle/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testFindTestRun(self):
        data = {
            "data":{
                "CycleName": "CycleName01",
                "Project": "Project01",
                "CycleLevel": "SMK",
            }
        }
        rep = self.c.post(path='/cccs/api/find_run/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddTRComments(self):
        data = {
            "data":{
                "TestRunName": "TestRunName01",
                "Comments": "........",
            }
        }
        rep = self.c.post(path='/cccs/api/add_comment/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChgCycleStatus(self):
        data = {
            "data":{
                "CycleName": "CycleName01",
                "Status": "ACTIVE",
            }
        }
        rep = self.c.post(path='/cccs/api/change_cyc_status/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChgPlanCaseStatus(self):
        data = {
            "data":{
                "CycleName": "CycleName01",
                "CaseName": "CaseName01",
                "Status": "ACTIVE",
            }
        }
        rep = self.c.post(path='/cccs/api/change_plc_status/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)
