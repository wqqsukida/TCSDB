# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 5/8/19 2:41 PM
# FileName: api.py
from utils.auth_token import APIAuthView,APITokenAuthView
from django.shortcuts import HttpResponse
from django.db import transaction
import json,traceback
import datetime
from monitor.models import *
from django.db.models import Max
from django.conf import settings

TEST = settings.TESTING

class AddDUTNodes(APIAuthView):
    '''
    增加一个DUT信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            DUTInfo.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeDUTFW(APIAuthView):
    '''
    更新DUT FW信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            with transaction.atomic():
                sn = res.pop('SerialNum')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                dut_obj.update(**res)
                res['Operator'] = 'Test' if TEST  else request.session['api_auth'].get("user")
                DUTFW.objects.create(**res, DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeDUTHost(APIAuthView):
    '''
    更新DUT Host信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            with transaction.atomic():
                sn = res.pop('SerialNum')
                slot = res.get('SlotID')
                hostname = res.get('HostName')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                slot_obj = SlotInfo.objects.filter(HostID__HostName=hostname,SlotID=slot)
                dut_obj.update(HostName=hostname,SlotID=slot_obj.first())
                res['Operator'] = 'Test' if TEST else request.session['api_auth'].get("user")
                DUTHost.objects.create(**res, DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeDUTBasicInfo(APIAuthView):
    '''
    修改DUT基本信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            sn = res.pop('SerialNum')
            dut_obj = DUTInfo.objects.filter(SerialNum=sn)
            dut_obj.update(**res)
            response = {'code': 0, 'msg': 'Success!', 'data': True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class AddDUTMonitorRec(APIAuthView):
    '''
    增加一次DUT健康监控记录
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            with transaction.atomic():
                sn = res.pop('SerialNum')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                res['Operator'] = 'Test' if TEST else request.session['api_auth'].get("user")
                DUTMonitor.objects.create(**res, DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetDUTBasicInfo(APIAuthView):
    '''
    获得DUT基本信息（包含FW版本和Host信息）
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            sn = res.get('SerialNum')
            dut_obj = DUTInfo.objects.filter(SerialNum=sn)
            data = dut_obj.values('SerialNum','DeviceType','Manufacture','ModelNum','EUI',
                                   'Interface','ProductName','RawCapacity','UserCapacity',
                                   'Notes','FWLoaderRev','GoldenFWRev','FWRev',
                                   'HostName').first()
            data['Manufactured'] = dut_obj.first().Manufactured.strftime("%Y-%m-%d %H:%m:%s")
            # slot_num_obj = DUTHost.objects.filter(DUTID=dut_obj.first())
            # if slot_num_obj:
            # data['SlotID'] = slot_num_obj.order_by("Changed").last().SlotID
            if dut_obj.first().SlotID:
                data['SlotID'] = dut_obj.first().SlotID.SlotID
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class GetDUTHealthInfo(APIAuthView):
    '''
    获得DUT健康信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            sn = res.get('SerialNum')
            dut_obj = DUTInfo.objects.get(SerialNum=sn)
            monitor_obj = DUTMonitor.objects.filter(DUTID=dut_obj)
            data = monitor_obj.values('CurrentPower','T1','T2','AvgAging','HostWrtten','HostRead',
                                      'PowerCycles','PowerOnHours','UnsafeShutdowns','MediaErrNum',
                                      'ErrLogNum','PCIE','Vendor_INFO1','Vendor_INFO2','Vendor_INFO3'
                                      ).last()
            if data:
                data['SerialNum'] = sn
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class GetAllDUTByHostName(APIAuthView):
    '''
    获得主机上所有DUT的SN
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            hostname = res.get('HostName')
            data = DUTInfo.objects.filter(SlotID__HostID__HostName=hostname).values('SerialNum')
            data = [i.get("SerialNum") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class GetAllDUTByGroupID(APIAuthView):
    '''
    获得同组的所有DUT的SN
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            gid = res.get("GroupID")
            data = DUTInfo.objects.filter(GroupID=gid).values("SerialNum")
            data = [i.get("SerialNum") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class GetAllDUTByTag(APIAuthView):
    '''
    获得相同标签的所有DUT的SN
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            tags = res.get("Tags")
            data = DUTInfo.objects.filter(Tags=tags).values("SerialNum")
            data = [i.get("SerialNum") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class FindDuts(APIAuthView):
    '''
    查询所有符合条件的DUT的SN
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            product_name = res.get("ProductName")
            hostname = res.get("HostName")
            interface = res.get("Interface")
            raw_capacity = res.get("RawCapacity")
            user_capacity = res.get("UserCapacity")
            parms_dict = {}
            if product_name and product_name != "ALL":
                parms_dict["ProductName"] = product_name
            if hostname and hostname != "ALL":
                parms_dict["HostName"] = hostname
            if interface and interface != "ALL":
                parms_dict["Interface"] = interface
            if raw_capacity and raw_capacity != 0:
                parms_dict["RawCapacity"] = raw_capacity
            if user_capacity and user_capacity != 0:
                parms_dict["UserCapacity"] = user_capacity
            data = DUTInfo.objects.filter(**parms_dict).values("SerialNum")
            data = [i.get("SerialNum") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class ChangeDUTGroupID(APIAuthView):
    '''
    更新DUT的GroupID信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            with transaction.atomic():
                sn = res.get('SerialNum')
                gid = res.get('GroupID')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                dut_obj.update(GroupID=gid)
                operator = 'Test' if TEST else request.session['api_auth'].get("user")
                DUTGrp.objects.create(GroupID=gid, Operator=operator,DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeDUTTags(APIAuthView):
    '''
    更新DUT的Tag信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            with transaction.atomic():
                sn = res.get('SerialNum')
                tags = res.get('Tags')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                dut_obj.update(Tags=tags)
                operator = 'Test' if TEST else request.session['api_auth'].get("user")
                DUTGrp.objects.create(Tags=tags, Operator=operator,DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeDUTStatus(APIAuthView):
    '''
    更新DUT的状态
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            sn = res.get('SerialNum')
            status = res.get("Status")
            dut_obj = DUTInfo.objects.filter(SerialNum=sn)
            dut_obj.update(Status=status)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetDUTStatus(APIAuthView):
    '''
    获得DUT的状态
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            sn = res.get('SerialNum')
            status = DUTInfo.objects.get(SerialNum=sn).Status
            response = {'code':0,'msg':'Success!','data':{"Status":status}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetDUTTags(APIAuthView):
    '''
    获得DUT的Tags
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            sn = res.get('SerialNum')
            tags = DUTInfo.objects.get(SerialNum=sn).Tags
            response = {'code':0,'msg':'Success!','data':{"Tags":tags}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetDUTGroupID(APIAuthView):
    '''
    获得DUT的GroupID
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            sn = res.get('SerialNum')
            gid = DUTInfo.objects.get(SerialNum=sn).GroupID
            response = {'code':0,'msg':'Success!','data':{"GroupID":gid}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

########################################################################################################################
class AddHostInfo(APIAuthView):
    '''
    新增Host机器信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            HostInfo.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeHostHWInfo(APIAuthView):
    '''
    更新Host机器硬件配置信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.pop("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            host_obj.update(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeHostNetInfo(APIAuthView):
    '''
    更新Host机器网络配置信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.pop("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            host_obj.update(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeSlotDUTInfo(APIAuthView):
    '''
    新增/更新Slot信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.pop("HostName")
            slot = res.get("SlotID")
            host_obj = HostInfo.objects.filter(HostName=host_name).first()
            # 如果存在HostID=host_obj,SlotID=slot的数据,则修改;不存在则添加
            SlotInfo.objects.update_or_create(HostID=host_obj,SlotID=slot,defaults=res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeHostOSInfo(APIAuthView):
    '''
    更新Host机器OS信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.pop('HostName')
            host_obj = HostInfo.objects.filter(HostName=host_name)
            operator = 'Test' if TEST else request.session['api_auth'].get("user")
            HostOS.objects.create(**res,Operator=operator,HostID=host_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeHostDriverInfo(APIAuthView):
    '''
    新增/更新Host机器驱动信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.pop("HostName")
            hw = res.get("Hardware")
            os_obj = HostOS.objects.filter(HostID__HostName=host_name).order_by("Changed").last()
            operator = 'Test' if TEST else request.session['api_auth'].get("user")
            res['Operator'] = operator
            HostDriver.objects.create(OSID=os_obj,**res)
            # 如果存在HostID=host_obj,Hardware=hw的数据,则修改;不存在则添加
            # HostDriver.objects.update_or_create(OSID=os_obj,Hardware=hw,defaults=res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeHostBasicInfo(APIAuthView):
    '''
    修改Host机器的基本信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.pop("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            host_obj.update(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))


class AddHostMonitorRec(APIAuthView):
    '''
    新增一条Host机器的健康状态监控记录
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.pop("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            operator = 'Test' if TEST else request.session['api_auth'].get("user")
            res['Operator'] = operator
            HostMonitor.objects.create(**res,HostID=host_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChangeHostSWInfo(APIAuthView):
    '''
    新增/更新Host机器上测试软件安装信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.pop("HostName")
            tool_name = res.get("ToolName")
            os_obj = HostOS.objects.filter(HostID__HostName=host_name).order_by("Changed").last()
            operator = 'Test' if TEST else request.session['api_auth'].get("user")
            res['Operator'] = operator
            HostSoftware.objects.create(OSID=os_obj,**res)
            # 如果存在HostID=host_obj,Hardware=hw的数据,则修改;不存在则添加
            # HostSoftware.objects.update_or_create(OSID=os_obj,ToolName=tool_name,defaults=res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetHostBasicInfo(APIAuthView):
    '''
    获得Host机器的基本信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            data = host_obj.values("HostName","Manufacture","DeviceModel","DeviceType",
                                   "IPV4Addr").first()
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetHostHWInfo(APIAuthView):
    '''
    获得Host机器的硬件信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            data = host_obj.values("HostName","MotherBoard","CPUType","NumOfCPU",
                                   "MaxCPUNum","CPUCores","DRAMType","DRAMSize",
                                   "MaxDRAMSize","MaxSATASlot","MaxAICSlot",
                                   "MaxU2Slot").first()
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetHostNetInfo(APIAuthView):
    '''
    获得Host机器的网络配置信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            data = host_obj.values("HostName","MAC","IPV4Addr","NICType",
                                   "WIFISupported","IPV4WIFI").first()
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetHostOSInfo(APIAuthView):
    '''
    获得Host机器的OS信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            data = HostOS.objects.filter(HostID__HostName=host_name).values(
                "OSType","OSVersion"
            ).order_by("Changed").last()
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetHostDriverInfo(APIAuthView):
    '''
    获得Host机器的驱动信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            os_obj = HostOS.objects.filter(HostID__HostName=host_name).order_by("Changed").last()
            # 分组获取当前os下，每个Hardware对应的dirver的最新时间max_time
            data = HostDriver.objects.filter(OSID=os_obj).values("Hardware").annotate(max_time=Max("Changed"))
            res = {}
            for i in data:
                val_obj = HostDriver.objects.get(Changed=i.get("max_time"), Hardware=i.get("Hardware"))
                res[i.get("Hardware")] = [val_obj.DriverName,val_obj.DriverVersion]
            response = {'code': 0, 'msg': 'Success!', 'data': res}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetHostToolsInfo(APIAuthView):
    '''
    获得Host机器的工具版本信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            os_obj = HostOS.objects.filter(HostID__HostName=host_name).order_by("Changed").last()
            # 分组获取当前os下，每个Hardware对应的dirver的最新时间max_time
            data = HostSoftware.objects.filter(OSID=os_obj).values("ToolName").annotate(max_time=Max("Changed"))
            res = {}
            for i in data:
                val_obj = HostSoftware.objects.get(Changed=i.get("max_time"), ToolName=i.get("ToolName"))
                res[i.get("ToolName")] = val_obj.ToolVer
            response = {'code': 0, 'msg': 'Success!', 'data': res}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetHostCurStatus(APIAuthView):
    '''
    获得Host机器当前的硬件使用状态
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            data = HostMonitor.objects.filter(HostID__HostName=host_name).values(
                "CPUUsage","RAMUsage","DISKUsage","NetworkConnection",
                "NetworkUsage","TotalProcesses"
            ).order_by("Changed").last()
            data["HostName"] = host_name
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetAllSlotsByHostName(APIAuthView):
    '''
    获得Host机器上所有Slot的信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            data = SlotInfo.objects.filter(HostID__HostName=host_name).values('id','SlotID')
            res = {}
            for i in data:
                dut_obj = DUTInfo.objects.filter(SlotID=i.get("id"))
                if dut_obj :
                    res[i.get("SlotID")] = dut_obj.first().SerialNum
                else:
                    res[i.get("SlotID")] = None
            response = {'code': 0, 'msg': 'Success!', 'data': res}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class FindHosts(APIAuthView):
    '''
    获得符合条件的Host机器列表
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            device_model = res.get("DeviceModel")
            status = res.get("Status")
            parms_dict = {}
            if device_model and device_model != "ALL":
                parms_dict["DeviceModel"] = device_model
            if status and status != "ALL":
                parms_dict["Status"] = status

            data = HostInfo.objects.filter(**parms_dict).values("HostName")
            data = [i.get("HostName") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class GetDisconnectedHost(APIAuthView):
    '''
    获得掉线的Host机器清单
    '''
    def post(self,request,*args,**kwargs):
        try:
            host_obj = HostInfo.objects.filter(Status='BAD')
            data = [i.HostName for i in host_obj]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetHostStatus(APIAuthView):
    '''
    获取当前主机状态
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            data = {'Status':host_obj.first().Status}
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Service internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class ChangHostStatus(APIAuthView):
    '''
    修改当前主机的状态
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            host_name = res.get("HostName")
            status = res.get("Status")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            host_obj.update(Status=status)
            response = {'code': 0, 'msg': 'Success!', 'data': True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Service internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

########################################################################################################################
class AddSrtPkg(APIAuthView):
    '''
    新增Script包信息记录
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            ScriptPackage.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class AddSrtInfo(APIAuthView):
    '''
    新增Script信息记录
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.pop("PkgName")
            pkg_obj = ScriptPackage.objects.filter(PkgName=pkg_name)
            ScriptSrtInfo.objects.create(**res,PKGID=pkg_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChgSrtPkgLabels(APIAuthView):
    '''
    新增/更新Script Package的标签
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.get("PkgName")
            labels = res.get("Labels")
            pkg_obj = ScriptPackage.objects.filter(PkgName=pkg_name)
            pkg_obj.update(Labels=labels)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetSrtPkg(APIAuthView):
    '''
    获得Package的信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.get("PkgName")
            pkg_obj = ScriptPackage.objects.filter(PkgName=pkg_name)
            data = pkg_obj.values("PkgName","Project","PkgPath","Labels").first()
            data["Date"] = pkg_obj.first().Date.strftime('%Y-%m-%d %H:%m:%s')
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetPkgSrtList(APIAuthView):
    '''
    获得Package下Script的信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.get("PkgName")
            pkg_obj = ScriptPackage.objects.filter(PkgName=pkg_name)
            data = pkg_obj.first().scriptsrtinfo_set.values("SrtName","GitRepo",
                                                            "GitBranch","GitCommitID")
            response = {'code': 0, 'msg': 'Success!', 'data': list(data)}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))


class FindSrtPkg(APIAuthView):
    '''
    查找对应的Script Package
    '''
    def post(self, request, *args, **kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            project = res.get("Project")
            labels = res.get("Labels")
            timeDelta = res.get("timeDelta")
            parms_dict = {}
            if project and project != "ALL":
                parms_dict["Project"] = project
            if labels:
                parms_dict["Labels"] = labels

            data = ScriptPackage.objects.filter(**parms_dict).values()
            if timeDelta:
                _timeDelta = datetime.datetime.now() - datetime.timedelta(days=timeDelta)
                data = data.filter(Date__gt=_timeDelta)
            data = [i.get("PkgName") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

########################################################################################################################
class AddFWPkg(APIAuthView):
    '''
    新增FW Bin包信息记录
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            FWPackage.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class AddFWBin(APIAuthView):
    '''
    新增FWBinary信息记录
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.pop("PkgName")
            pkg_obj = FWPackage.objects.filter(PkgName=pkg_name)
            FWBinary.objects.create(**res,PKGID=pkg_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class AddFWRel(APIAuthView):
    '''
    新增FW Release信息记录
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.pop("PkgName")
            pkg_obj = FWPackage.objects.filter(PkgName=pkg_name)
            FWRelease.objects.create(**res,PKGID=pkg_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class ChgFWPkgLabels(APIAuthView):
    '''
    新增/改变FW Package的标签
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.get("PkgName")
            labels = res.get("Labels")
            pkg_obj = FWPackage.objects.filter(PkgName=pkg_name)
            pkg_obj.update(Labels=labels)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetFWBins(APIAuthView):
    '''
    获得Package的Bin信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.get("PkgName")
            pkg_obj = FWPackage.objects.filter(PkgName=pkg_name)
            data = pkg_obj.first().fwbinary_set.values("SrtName","GitRepo","BinaryType",
                                                       "GitBranch","GitCommitID")
            response = {'code': 0, 'msg': 'Success!', 'data': list(data)}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetFWPackes(APIAuthView):
    '''
    获得Package的信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.get("PkgName")
            pkg_obj = FWPackage.objects.filter(PkgName=pkg_name)
            data = pkg_obj.values("PkgName","Project","External","PkgType","PkgPath","Labels").first()
            data["Date"] = pkg_obj.first().Date.strftime('%Y-%m-%d %H:%m:%s')
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class GetFWRels(APIAuthView):
    '''
    获得Release的信息
    '''
    def post(self,request,*args,**kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            rel_name = res.get("RelName")
            pkg_obj = FWRelease.objects.filter(Name=rel_name)
            data = pkg_obj.values("Name","TRName","Version").first()
            data["Date"] = pkg_obj.first().Date.strftime('%Y-%m-%d %H:%m:%s')
            data["PkgName"] = pkg_obj.first().PKGID.PkgName
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response))

class FindFWPkgList(APIAuthView):
    '''
    获得符合条件的FW Package列表
    '''
    def post(self, request, *args, **kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            project = res.get("Project")
            external = res.get("External")
            pkg_type = res.get("PkgType")
            labels = res.get("Labels")
            timeDelta = res.get("timeDelta")
            parms_dict = {}
            if project and project != "ALL":
                parms_dict["Project"] = project
            if external:
                parms_dict["External"] = external
            if pkg_type and pkg_type != "ALL":
                parms_dict["PkgType"] = pkg_type
            if labels:
                parms_dict["Labels"] = labels

            data = FWPackage.objects.filter(**parms_dict).values()
            if timeDelta:
                _timeDelta = datetime.datetime.now() - datetime.timedelta(days=timeDelta)
                data = data.filter(Date__gt=_timeDelta)
            data = [i.get("PkgName") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))

class FindFWRelList(APIAuthView):
    '''
    获得符合条件的FW Release列表
    '''
    def post(self, request, *args, **kwargs):
        res = json.loads(request.body.decode('utf-8')).get("data")
        try:
            pkg_name = res.get("PkgName")
            test_run_name = res.get("TestRunName")
            timeDelta = res.get("timeDelta")
            data = FWRelease.objects.all().values()
            if pkg_name and pkg_name != "ALL":
                data = data.filter(PKGID__PkgName=pkg_name)
            if test_run_name:
                data = data.filter(TRName=test_run_name)
            if timeDelta:
                _timeDelta = datetime.datetime.now() - datetime.timedelta(days=timeDelta)
                data = data.filter(Date__gt=_timeDelta)
            data = [i.get("Name") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response))
