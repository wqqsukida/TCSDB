# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 5/8/19 2:41 PM
# FileName: api.py
from utils.auth_token import APIAuthView
from django.shortcuts import HttpResponse
from django.db import transaction
import json,traceback
from monitor.models import *
from django.db.models import Max

class AddDUTNodes(APIAuthView):
    '''
    增加一个DUT信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            DUTInfo.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeDUTFW(APIAuthView):
    '''
    更新DUT FW信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            with transaction.atomic():
                sn = res.pop('SerialNum')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                dut_obj.update(**res)
                res['Operator'] = request.session['api_auth'].get("user")    # 添加Operator字段
                DUTFW.objects.create(**res, DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeDUTHost(APIAuthView):
    '''
    更新DUT Host信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            with transaction.atomic():
                sn = res.pop('SerialNum')
                slot = res.get('SlotID')
                hostname = res.get('HostName')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                slot_obj = SlotInfo.objects.filter(HostID__HostName=hostname,SlotID=slot)
                dut_obj.update(HostName=hostname,SlotID=slot_obj.first())
                res['Operator'] = request.session['api_auth'].get("user")    # 添加Operator字段
                DUTHost.objects.create(**res, DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class AddDUTMonitorRec(APIAuthView):
    '''
    增加一次DUT健康监控记录
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            with transaction.atomic():
                sn = res.pop('SerialNum')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                res['Operator'] = request.session['api_auth'].get("user")    # 添加Operator字段
                DUTMonitor.objects.create(**res, DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetDUTBasicInfo(APIAuthView):
    '''
    获得DUT基本信息（包含FW版本和Host信息）
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            sn = res.get('SerialNum')
            print(sn)
            dut_obj = DUTInfo.objects.filter(SerialNum=sn)
            data = dut_obj.values('SerialNum','DeviceType','Manufacture','ModelNum','EUI',
                                   'Interface','ProductName','RawCapacity','UserCapacity',
                                   'Manufactured','Notes','FWLoaderRev','GoldenFWRev','FWRev',
                                   'HostName').first()
            slot_num_obj = DUTHost.objects.filter(DUTID=dut_obj.first())
            if slot_num_obj:
                data['SlotID'] = slot_num_obj.order_by("Changed").last().SlotID
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response,indent=4))

class GetDUTHealthInfo(APIAuthView):
    '''
    获得DUT健康信息
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            sn = res.get('SerialNum')
            dut_obj = DUTInfo.objects.get(SerialNum=sn)
            monitor_obj = DUTMonitor.objects.filter(DUTID=dut_obj)
            data = monitor_obj.values('CurrentPower','T1','T2','AvgAging','HostWrtten','HostRead',
                                      'PowerCycles','PowerOnHours','UnsafeShutdowns','MediaErrNum',
                                      'ErrLogNum','PCIE','Vendor_INFO1','Vendor_INFO2','Vendor_INFO3'
                                      ).last()
            data['SerialNum'] = sn
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response,indent=4))

class GetAllDUTByHostName(APIAuthView):
    '''
    获得主机上所有DUT的SN
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            hostname = res.get('HostName')
            data = DUTInfo.objects.filter(SlotID__HostID__HostName=hostname).values('SerialNum')
            data = [i.get("SerialNum") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response,indent=4))

class GetAllDUTByGroupID(APIAuthView):
    '''
    获得同组的所有DUT的SN
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            gid = res.get("GroupID")
            data = DUTInfo.objects.filter(GroupID=gid).values("SerialNum")
            data = [i.get("SerialNum") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response,indent=4))

class GetAllDUTByTag(APIAuthView):
    '''
    获得相同标签的所有DUT的SN
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            tags = res.get("Tags")
            data = DUTInfo.objects.filter(Tags=tags).values("SerialNum")
            data = [i.get("SerialNum") for i in data]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response,indent=4))

class FindDuts(APIAuthView):
    '''
    查询所有符合条件的DUT的SN
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
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
        return HttpResponse(json.dumps(response,indent=4))

class ChangeDUTGroupID(APIAuthView):
    '''
    更新DUT的GroupID信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            with transaction.atomic():
                sn = res.get('SerialNum')
                gid = res.get('GroupID')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                dut_obj.update(GroupID=gid)
                operator = request.session['api_auth'].get("user")
                DUTGrp.objects.create(GroupID=gid, Operator=operator,DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeDUTTags(APIAuthView):
    '''
    更新DUT的Tag信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            with transaction.atomic():
                sn = res.get('SerialNum')
                tags = res.get('Tags')
                dut_obj = DUTInfo.objects.filter(SerialNum=sn)
                dut_obj.update(Tags=tags)
                operator = request.session['api_auth'].get("user")
                DUTGrp.objects.create(Tags=tags, Operator=operator,DUTID=dut_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeDUTStatus(APIAuthView):
    '''
    更新DUT的状态
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            sn = res.get('SerialNum')
            status = res.get("Status")
            dut_obj = DUTInfo.objects.filter(SerialNum=sn)
            dut_obj.update(Status=status)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetDUTStatus(APIAuthView):
    '''
    获得DUT的状态
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            sn = res.get('SerialNum')
            status = DUTInfo.objects.get(SerialNum=sn).Status
            response = {'code':0,'msg':'Success!','data':{"Status":status}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetDUTTags(APIAuthView):
    '''
    获得DUT的Tags
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            sn = res.get('SerialNum')
            tags = DUTInfo.objects.get(SerialNum=sn).Tags
            response = {'code':0,'msg':'Success!','data':{"Tags":tags}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetDUTGroupID(APIAuthView):
    '''
    获得DUT的GroupID
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            sn = res.get('SerialNum')
            gid = DUTInfo.objects.get(SerialNum=sn).GroupID
            response = {'code':0,'msg':'Success!','data':{"GroupID":gid}}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

########################################################################################################################
class AddHostInfo(APIAuthView):
    '''
    新增Host机器信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            HostInfo.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeHostHWInfo(APIAuthView):
    '''
    更新Host机器硬件配置信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.pop("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            host_obj.update(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeHostNetInfo(APIAuthView):
    '''
    更新Host机器网络配置信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.pop("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            host_obj.update(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeSlotDUTInfo(APIAuthView):
    '''
    新增/更新Slot信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
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
        return HttpResponse(json.dumps(response,indent=4))

class ChangeHostOSInfo(APIAuthView):
    '''
    更新Host机器OS信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.pop('HostName')
            host_obj = HostInfo.objects.filter(HostName=host_name)
            operator = request.session['api_auth'].get("user")
            HostOS.objects.create(**res,Operator=operator,HostID=host_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeHostDriverInfo(APIAuthView):
    '''
    新增/更新Host机器驱动信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.pop("HostName")
            hw = res.get("Hardware")
            os_obj = HostOS.objects.filter(HostID__HostName=host_name).order_by("Changed").last()
            operator = request.session['api_auth'].get("user")
            res['Operator'] = operator
            HostDriver.objects.create(OSID=os_obj,**res)
            # 如果存在HostID=host_obj,Hardware=hw的数据,则修改;不存在则添加
            # HostDriver.objects.update_or_create(OSID=os_obj,Hardware=hw,defaults=res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class AddHostMonitorRec(APIAuthView):
    '''
    新增一条Host机器的健康状态监控记录
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.pop("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            operator = request.session['api_auth'].get("user")
            res['Operator'] = operator
            HostMonitor.objects.create(**res,HostID=host_obj.first())
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class ChangeHostSWInfo(APIAuthView):
    '''
    新增/更新Host机器上测试软件安装信息
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.pop("HostName")
            tool_name = res.get("ToolName")
            os_obj = HostOS.objects.filter(HostID__HostName=host_name).order_by("Changed").last()
            operator = request.session['api_auth'].get("user")
            res['Operator'] = operator
            HostSoftware.objects.create(OSID=os_obj,**res)
            # 如果存在HostID=host_obj,Hardware=hw的数据,则修改;不存在则添加
            # HostSoftware.objects.update_or_create(OSID=os_obj,ToolName=tool_name,defaults=res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetHostBasicInfo(APIAuthView):
    '''
    获得Host机器的基本信息
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.get("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            data = host_obj.values("HostName","Manufacture","DeviceModel","DeviceType",
                                   "IPV4Addr").first()
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetHostHWInfo(APIAuthView):
    '''
    获得Host机器的硬件信息
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
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
        return HttpResponse(json.dumps(response,indent=4))

class GetHostNetInfo(APIAuthView):
    '''
    获得Host机器的网络配置信息
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.get("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            data = host_obj.values("HostName","MAC","IPV4Addr","NICType",
                                   "WIFISupported","IPV4WIFI").first()
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetHostOSInfo(APIAuthView):
    '''
    获得Host机器的OS信息
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.get("HostName")
            data = HostOS.objects.filter(HostID__HostName=host_name).values(
                "OSType","OSVersion"
            ).order_by("Changed").last()
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetHostDriverInfo(APIAuthView):
    '''
    获得Host机器的驱动信息
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
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
        return HttpResponse(json.dumps(response,indent=4))

class GetHostToolsInfo(APIAuthView):
    '''
    获得Host机器的工具版本信息
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
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
        return HttpResponse(json.dumps(response,indent=4))

class GetHostCurStatus(APIAuthView):
    '''
    获得Host机器当前的硬件使用状态
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
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
        return HttpResponse(json.dumps(response,indent=4))

class GetAllSlotsByHostName(APIAuthView):
    '''
    获得Host机器上所有Slot的信息
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
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
        return HttpResponse(json.dumps(response,indent=4))

class FindHosts(APIAuthView):
    '''
    获得符合条件的Host机器列表
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
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
        return HttpResponse(json.dumps(response,indent=4))

class GetDisconnectedHost(APIAuthView):
    '''
    获得掉线的Host机器清单
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_obj = HostInfo.objects.filter(Status='BAD')
            data = [i.get("HostName") for i in host_obj]
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return HttpResponse(json.dumps(response,indent=4))

class GetHostStatus(APIAuthView):
    '''
    获取当前主机状态
    '''
    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.get("HostName")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            data = {'Status':host_obj.first().Status}
            response = {'code': 0, 'msg': 'Success!', 'data': data}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Service internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response, indent=4))

class ChangHostStatus(APIAuthView):
    '''
    修改当前主机的状态
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        try:
            host_name = res.get("HostName")
            status = res.get("Status")
            host_obj = HostInfo.objects.filter(HostName=host_name)
            host_obj.update(Status=status)
            response = {'code': 0, 'msg': 'Success!', 'data': True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Service internal error:{0}'.format(str(e)), 'data': {}}
        return HttpResponse(json.dumps(response, indent=4))