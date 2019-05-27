from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import json
import copy
import traceback
from utils.pagination import Pagination
from monitor.models import *
from django.db.models import Q

def init_paginaion(request,queryset):
    # 初始化分页器
    query_params = copy.deepcopy(request.GET)  # QueryDict
    current_page = request.GET.get('page', 1)
    # per_page = config.per_page
    # pager_page_count = config.pager_page_count
    if isinstance(queryset,list):
        all_count = len(queryset)
    else:
        all_count = queryset.count()
    base_url = request.path_info
    page_obj = Pagination(current_page, all_count, base_url, query_params)
    query_set = queryset[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()

    return query_set,page_html

def duts(request):
    '''
    DUT列表
    :param request:
    :return:
    '''
    if request.method == "GET":
        page = request.GET.get("page")
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_q = request.GET.get('q','')

        queryset = DUTInfo.objects.filter(Q(Q(SerialNum__contains=search_q) |
                                           Q(HostName__contains=search_q) |
                                           Q(ProductName__contains=search_q) |
                                           Q(Interface__contains=search_q) |
                                           Q(RawCapacity__contains=search_q) |
                                           Q(UserCapacity__contains=search_q))
                                          ).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'monitor/duts.html',locals())

def dut_update(request):
    '''
    更新DUT信息
    :param request:
    :return:
    '''
    if request.method == "GET":
        res = {}
        id = request.GET.get("sid",None)

        dut_obj = DUTInfo.objects.filter(id=id)

        dut_dict = dut_obj.values().first()
        if dut_dict:
            res = dict(dut_dict)
            res.pop("Manufactured")
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        page = request.POST.get('page')
        id = request.POST.get("id",None)
        DeviceType = request.POST.get("DeviceType",None)
        Manufacture = request.POST.get("Manufacture",None)
        ModelNum = request.POST.get("ModelNum",None)
        EUI = request.POST.get("EUI",None)
        Interface = request.POST.get("Interface",None)
        ProductName = request.POST.get("ProductName",None)
        RawCapacity = request.POST.get("RawCapacity",None)
        UserCapacity = request.POST.get("UserCapacity",None)
        Status = request.POST.get("Status",None)
        Notes = request.POST.get("Notes",None)
        form_data = {'DeviceType': DeviceType, 'Manufacture': Manufacture, 'ModelNum': ModelNum,
                     'EUI': EUI, 'Interface': Interface, 'ProductName': ProductName,
                     'RawCapacity': RawCapacity, 'UserCapacity': UserCapacity,
                     'Status': Status, 'Notes': Notes}
        try:
            DUTInfo.objects.filter(id=id).update(**form_data)
            result = {"code": 0, "message": "更新设备成功！"}
        except Exception as e:
            print(traceback.format_exc())
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/duts?status={0}&message={1}&page={2}'.
                            format(result.get("code", ""),
                                   result.get("message", ""),
                                   page))

def hosts(request):
    '''
    主机列表
    :param request:
    :return:
    '''
    if request.method == "GET":
        page = request.GET.get("page")
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_q = request.GET.get('q','')

        queryset = HostInfo.objects.filter(Q(Q(HostName__contains=search_q) |
                                           Q(Manufacture__contains=search_q) |
                                           Q(DeviceModel__contains=search_q) |
                                           Q(DeviceType__contains=search_q) |
                                           Q(Status__contains=search_q) |
                                           Q(MotherBoard__contains=search_q))
                                          ).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'monitor/hosts.html',locals())

def host_update(request):
    '''
    更新主机信息
    :param request:
    :return:
    '''
    if request.method == "GET":
        res = {}
        id = request.GET.get("hid",None)

        host_obj = HostInfo.objects.filter(id=id)

        host_dict = host_obj.values().first()
        if host_dict:
            res = dict(host_dict)
            res.pop("JoininDate")
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        page = request.POST.get('page')
        id = request.POST.get("id",None)
        Manufacture = request.POST.get("Manufacture",None)
        DeviceModel = request.POST.get("DeviceModel",None)
        DeviceType = request.POST.get("DeviceType",None)
        MotherBoard = request.POST.get("MotherBoard",None)
        MaxSATASlot = request.POST.get("MaxSATASlot",None)
        MaxAICSlot = request.POST.get("MaxAICSlot",None)
        MaxU2Slot = request.POST.get("MaxU2Slot",None)
        Status = request.POST.get("Status",None)
        form_data = {'Manufacture': Manufacture, 'DeviceModel': DeviceModel, 'DeviceType': DeviceType,
                     'MotherBoard': MotherBoard, 'MaxSATASlot': MaxSATASlot, 'MaxAICSlot': MaxAICSlot,
                     'MaxU2Slot': MaxU2Slot, 'Status': Status }
        try:
            print(form_data)
            HostInfo.objects.filter(id=id).update(**form_data)
            result = {"code": 0, "message": "更新主机成功！"}
        except Exception as e:
            print(traceback.format_exc())
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/hosts?status={0}&message={1}&page={2}'.
                            format(result.get("code", ""),
                                   result.get("message", ""),
                                   page))

def asset_detail(request):
    result = {}
    if request.method == "GET":
        host_id = request.GET.get("id",None)
        host_obj = HostInfo.objects.filter(id=host_id).first()
        if host_obj:
            slot_query_list = SlotInfo.objects.filter(HostID=host_obj)

            result = {"code": 0, "message": "找到资产"}
        else:
            result = {"code": 1, "message": "未找到指定资产"}

        return render(request,'monitor/asset_detail.html',locals())

def dut_record(request):
    '''
    DUT操作历史记录
    :param request:
    :return:
    '''
    all_record = [

    ]
    if request.method == "GET":
        dut_id = request.GET.get("id",None)
        dut_obj = DUTInfo.objects.filter(id=dut_id).first()
        if dut_obj:
            fw_record = DUTFW.objects.filter(DUTID=dut_obj)
            host_record = DUTHost.objects.filter(DUTID=dut_obj)
            grp_record = DUTGrp.objects.filter(DUTID=dut_obj)
            for f in fw_record:all_record.append(f)
            for h in host_record:all_record.append(h)
            for g in grp_record:all_record.append(g)
            print(len(all_record))
            all_record = sorted(all_record,key=lambda x:x.Changed)
        all_record, page_html = init_paginaion(request, all_record)
        return render(request,'monitor/dut_record.html',locals())

def host_record(request):
    pass