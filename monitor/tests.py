from django.test import TestCase
from django.test import Client
from rest_framework.test import APIRequestFactory
import requests, json
import time
import hashlib
import inspect
import datetime
from requests.cookies import RequestsCookieJar
from django.conf import settings
from monitor.api import *
from monitor.models import *

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
        dut_obj = DUTInfo.objects.create(SerialNum="SerialNum01",DeviceType=5,Manufactured=datetime.datetime.now())
        DUTMonitor.objects.create(CurrentPower=1.1,T1=10,T2=10,DUTID=dut_obj)
        host_obj = HostInfo.objects.create(HostName="HostName01")
        slot_obj = SlotInfo.objects.create(SlotID=1,HostID=host_obj)
        HostOS.objects.create(OSType='OSType01',OSVersion='OSVersion01',HostID=host_obj)
        dut_obj.SlotID = slot_obj
        dut_obj.HostName = 'HostName01'
        dut_obj.GroupID = 1
        dut_obj.Tags = 'Tags01'
        dut_obj.save()


    def testAddDUTNodes(self):
        data = {
            "data":{
                "SerialNum": "SerialNum02",
                "DeviceType": 5,
                "Manufactured": "2019-05-16 16:50:37"
            }
        }
        rep = self.c.post(path='/monitor/api/dut/add/',content_type='application/json',data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeDUTFW(self):
        data = {
            "data":{
                "SerialNum": "SerialNum02",
                "FWLoaderRev": "FWLoaderRev02",
                "GoldenFWRev": "GoldenFWRev02",
                "FWRev": "FWRev02",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/change_fw/', content_type='application/json', data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeDUTHost(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
                "HostName": "HostName01",
                "SlotID": 1,
            }
        }
        rep = self.c.post(path='/monitor/api/dut/change_host/', content_type='application/json', data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddDUTMonitorRec(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
                "CurrentPower": 1.2,
                "T1": 20,
                "T2": 20,
            }
        }
        rep = self.c.post(path='/monitor/api/dut/add_monitor/', content_type='application/json', data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetDUTBasicInfo(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/get_info/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetDUTHealthInfo(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/get_monitor/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetAllDUTByHostName(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/get_by_host/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetAllDUTByGroupID(self):
        data = {
            "data":{
                "GroupID": 1,
            }
        }
        rep = self.c.post(path='/monitor/api/dut/get_by_grp/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetAllDUTByTag(self):
        data = {
            "data":{
                "Tags": "Tags01",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/get_by_tag/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testFindDuts(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/find/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeDUTGroupID(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
                "GroupID": 2,
            }
        }
        rep = self.c.post(path='/monitor/api/dut/change_grp/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeDUTTags(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
                "Tags": "Tags02",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/change_tag/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeDUTStatus(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
                "Status": "Idle",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/change_status/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)