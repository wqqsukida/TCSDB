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

        queryset = DUTInfo.objects.filter(Q(Q(HostName__contains=search_q) |
                                           Q(ProductName__contains=search_q) |
                                           Q(Interface__contains=search_q) |
                                           Q(RawCapacity__contains=search_q) |
                                           Q(UserCapacity__contains=search_q))
                                          ).distinct()
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


