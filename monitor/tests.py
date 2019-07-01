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
        os_obj = HostOS.objects.create(OSType='OSType01',OSVersion='OSVersion01',HostID=host_obj)
        HostDriver.objects.create(Hardware='Hardware01',DriverName='DriverName01',DriverVersion='DriverVersion01'
                                  ,OSID=os_obj)
        HostSoftware.objects.create(ToolName='ToolName01',ToolVer='ToolVer01',OSID=os_obj)
        HostMonitor.objects.create(CPUUsage=60,NetworkConnection=False,HostID=host_obj)
        dut_obj.SlotID = slot_obj
        dut_obj.HostName = 'HostName01'
        dut_obj.GroupID = 1
        dut_obj.Tags = 'Tags01'
        dut_obj.Status = 'Idle'
        dut_obj.save()
        host_obj.Status = 'BAD'
        host_obj.save()

        pkj_obj = ScriptPackage.objects.create(PkgName="PkgName",Project="Project01",PkgPath="PkgPath01")
        srt_obj = ScriptSrtInfo.objects.create(PKGID=pkj_obj,SrtName="SrtName01",GitRepo="GitRepo01")

        fw_pkg = FWPackage.objects.create(PkgName="PkgName01",Project="Project01",External=True,
                                          PkgType="DEBUG",PkgPath="PkgPath01")
        fw_bin = FWBinary.objects.create(PKGID=fw_pkg,BinaryName="BinaryName01",GitRepo="GitRepo01",
                                         GitBranch="GitBranch01",GitCommitID="GitCommitID01",
                                         BinaryType="GOLDEN")
        fw_rel = FWRelease.objects.create(PKGID=fw_pkg,TRName="TRName01",Date="2019-06-30 12:30:30",
                                          Version="Version01",Name="Name01")

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
                "SerialNum": "SerialNum01",
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

    def testGetDUTStatus(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/get_status/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetDUTTags(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/get_tag/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetDUTGroupID(self):
        data = {
            "data":{
                "SerialNum": "SerialNum01",
            }
        }
        rep = self.c.post(path='/monitor/api/dut/get_grp/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    ###################################################################################################
    def testAddHostInfo(self):
        data = {
            "data":{
                "HostName": "HostName02",
                "Manufacture": "Manufacture02",
                "DeviceModel": "DeviceModel02",
                "DeviceType": "Type02",
                "IPV4Addr": "192.168.0.1",
            }
        }
        rep = self.c.post(path='/monitor/api/host/add/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeHostHWInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
                "MotherBoard": "MotherBoard02",
                "CPUType": "CPUType02",
                "NumOfCPU": 2,
                "DRAMSize": "16GB",
            }
        }
        rep = self.c.post(path='/monitor/api/host/change_hw/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeHostNetInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
                "IPV4Addr": "192.168.0.2",
                "WIFISupported": True,
            }
        }
        rep = self.c.post(path='/monitor/api/host/change_net/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeSlotDUTInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
                "SlotID": 2,
                "Interface": "SATA",
                "Status": "Good",
            }
        }
        rep = self.c.post(path='/monitor/api/host/change_slot/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeHostOSInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
                "OSType": "OSType02",
                "OSVersion": "OSVersion02",
            }
        }
        rep = self.c.post(path='/monitor/api/host/change_os/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeHostDriverInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
                "Hardware": "Hardware02",
                "DriverName": "DriverName02",
                "DriverVersion": "DriverVersion02",
            }
        }
        rep = self.c.post(path='/monitor/api/host/change_driver/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddHostMonitorRec(self):
        data = {
            "data":{
                "HostName": "HostName01",
                "CPUUsage": 60,
                "NetworkConnection": True,
                "TotalProcesses": 51,
            }
        }
        rep = self.c.post(path='/monitor/api/host/add_monitor/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangeHostSWInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
                "ToolName": "ToolName02",
                "ToolVer": "ToolVer02",
            }
        }
        rep = self.c.post(path='/monitor/api/host/change_sw/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetHostBasicInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_info/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetHostHWInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_hw/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetHostNetInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_net/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetHostOSInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_os/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetHostDriverInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_driver/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetHostToolsInfo(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_sw/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetHostCurStatus(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_monitor/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetAllSlotsByHostName(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_slots/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testFindHosts(self):
        data = {
            "data":{
                "Status": "RETIRED",
            }
        }
        rep = self.c.post(path='/monitor/api/host/find/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetDisconnectedHost(self):
        rep = self.c.post(path='/monitor/api/host/disconnections/',content_type='application/json')
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetHostStatus(self):
        data = {
            "data":{
                "HostName": "HostName01",
            }
        }
        rep = self.c.post(path='/monitor/api/host/get_status/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChangHostStatus(self):
        data = {
            "data":{
                "HostName": "HostName01",
                "Status": "IDLE",
            }
        }
        rep = self.c.post(path='/monitor/api/host/change_status/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddSrtPkg(self):
        data = {
            "data":{
                "PkgName": "PkgName02",
                "Project": "Project02",
                "PkgPath": "PkgPath02",
            }
        }
        rep = self.c.post(path='/monitor/api/srt/add_pkg/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddSrtInfo(self):
        data = {
            "data":{
                "PkgName": "PkgName01",
                "SrtName": "SrtName02",
                "GitRepo": "GitRepo02",
            }
        }
        rep = self.c.post(path='/monitor/api/srt/add_srtinfo/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChgSrtPkgLabels(self):
        data = {
            "data":{
                "PkgName": "PkgName01",
                "Labels": "Labels01",
            }
        }
        rep = self.c.post(path='/monitor/api/srt/chg_lab/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetSrtPkg(self):
        data = {
            "data":{
                "PkgName": "PkgName01",
            }
        }
        rep = self.c.post(path='/monitor/api/srt/get_pkg/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetPkgSrtList(self):
        data = {
            "data":{
                "PkgName": "PkgName01",
            }
        }
        rep = self.c.post(path='/monitor/api/srt/get_srts/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testFindSrtPkg(self):
        data = {
            "data":{
                "Project": "Project01",
                "timeDelta": "1",
            }
        }
        rep = self.c.post(path='/monitor/api/srt/find_pkg/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddFWPkg(self):
        data = {
            "data":{
                "PkgName": "PkgName02",
                "Project": "Project02",
                "External": True,
                "PkgType": "DEBUG",
                "PkgPath": "PkgPath02"
            }
        }
        rep = self.c.post(path='/monitor/api/bin/add_pkg/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddFWBin(self):
        data = {
            "data":{
                "PkgName": "PkgName01",
                "BinaryType": "GOLDEN",
                "GitRepo": "GitRepo02",
                "GitBranch": "GitBranch02",
                "GitCommitID": "GitCommitID02",
                "BinaryName": "BinaryName02"
            }
        }
        rep = self.c.post(path='/monitor/api/bin/add_bin/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testAddFWRel(self):
        data = {
            "data":{
                "PkgName": "PkgName01",
                "Name": "Name02",
                "TRName": "TRName02",
                "Date": "2019-06-30 11:30:29",
                "Version": "Version02"
            }
        }
        rep = self.c.post(path='/monitor/api/bin/add_rel/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testChgFWPkgLabels(self):
        data = {
            "data":{
                "PkgName": "PkgName01",
                "Labels": "Labels01",
            }
        }
        rep = self.c.post(path='/monitor/api/bin/chg_lab/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetFWBins(self):
        data = {
            "data":{
                "PkgName": "PkgName01",
            }
        }
        rep = self.c.post(path='/monitor/api/bin/get_bins/',content_type='application/json'  ,data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetFWPackes(self):
        data = {
            "data": {
                "PkgName": "PkgName01",
            }
        }
        rep = self.c.post(path='/monitor/api/bin/get_pkgs/', content_type='application/json', data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testGetFWRels(self):
        data = {
            "data": {
                "RelName": "Name01",
            }
        }
        rep = self.c.post(path='/monitor/api/bin/get_rels/', content_type='application/json', data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testFindFWPkgList(self):
        data = {
            "data": {
                "Project": "ALL",
                "PkgType": "DEBUG"
            }
        }
        rep = self.c.post(path='/monitor/api/bin/find_pkg/', content_type='application/json', data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

    def testFindFWRelList(self):
        data = {
            "data": {
                "PkgName": "ALL",
                "TestRunName": "TRName01",
            }
        }
        rep = self.c.post(path='/monitor/api/bin/find_rel/', content_type='application/json', data=data)
        res = json.loads(rep.content)
        print(res)
        self.assertEqual(res.get("code"), 0)

