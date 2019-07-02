from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import json
import copy
import traceback
import datetime
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
    all_record = []
    if request.method == "GET":
        dut_id = request.GET.get("id",None)
        dut_obj = DUTInfo.objects.filter(id=dut_id).first()
        stime = request.GET.get("start_time","2019-01-01")
        etime = request.GET.get("end_time",datetime.datetime.now().strftime('%Y-%m-%d'))
        if dut_obj:
            fw_record = DUTFW.objects.filter(DUTID=dut_obj,Changed__range=(stime,etime))
            host_record = DUTHost.objects.filter(DUTID=dut_obj,Changed__range=(stime,etime))
            grp_record = DUTGrp.objects.filter(DUTID=dut_obj,Changed__range=(stime,etime))
            for f in fw_record:all_record.append(f)
            for h in host_record:all_record.append(h)
            for g in grp_record:all_record.append(g)
            # print(len(all_record))
            all_record = sorted(all_record,key=lambda x:x.Changed)
        all_record, page_html = init_paginaion(request, all_record)
        return render(request,'monitor/dut_record.html',locals())

def host_record(request):
    '''
    主机变更记录
    :param request:
    :return:
    '''
    all_record = []
    if request.method == "GET":
        host_id = request.GET.get("id",None)
        host_obj = HostInfo.objects.filter(id=host_id).first()
        stime = request.GET.get("start_time","2019-01-01")
        etime = request.GET.get("end_time",datetime.datetime.now().strftime('%Y-%m-%d'))
        if host_obj:
            all_record = HostOS.objects.filter(HostID=host_obj,Changed__range=(stime,etime))
            # print(len(all_record))
            # all_record = sorted(all_record,key=lambda x:x.Changed)
        all_record, page_html = init_paginaion(request, all_record)
        return render(request,'monitor/host_record.html',locals())

def os_record(request):
    '''
    OS变更记录
    :param request:
    :return:
    '''
    all_record = []
    if request.method == "GET":
        os_id = request.GET.get("id",None)
        os_obj = HostOS.objects.filter(id=os_id).first()
        host_obj = os_obj.HostID
        stime = request.GET.get("start_time","2019-01-01")
        etime = request.GET.get("end_time",datetime.datetime.now().strftime('%Y-%m-%d'))
        if os_obj:
            driver_record = HostDriver.objects.filter(OSID=os_obj,Changed__range=(stime,etime))
            sw_record = HostSoftware.objects.filter(OSID=os_obj,Changed__range=(stime,etime))
            for f in driver_record:all_record.append(f)
            for h in sw_record:all_record.append(h)
            # print(len(all_record))
            all_record = sorted(all_record,key=lambda x:x.Changed)
        all_record, page_html = init_paginaion(request, all_record)
        return render(request,'monitor/os_record.html',locals())

def package_list(request):
    '''
    script package列表
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

        queryset = ScriptPackage.objects.filter(Q(Q(PkgName__contains=search_q) |
                                           Q(Project__contains=search_q) |
                                           Q(Labels__contains=search_q))
                                          ).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'monitor/package_list.html',locals())

def add_package(request):
    if request.method == "POST":
        pkg_name = request.POST.get("PkgName")
        project = request.POST.get("Project")
        pkg_path = request.POST.get("PkgPath")
        page = request.POST.get("page")
        if pkg_name:
            try:
                ScriptPackage.objects.create(PkgName=pkg_name,Project=project,PkgPath=pkg_path)
                result = {"code": 0, "message": "Package创建成功!"}
            except Exception as e:
                result = {"code": 1, "message": str(e)}
        else:
            result = {"code": 1, "message": "必须指定名称!"}
        return HttpResponseRedirect('/monitor/package_list?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page))

def update_package(request):
    if request.method == "GET":
        pid = request.GET.get('pid',None)
        pkg_obj = ScriptPackage.objects.filter(id=pid)
        pkg_dict = pkg_obj.values('id','PkgName','Project','PkgPath','Labels').first()
        # print(pkg_dict)
        return HttpResponse(json.dumps(dict(pkg_dict)))

    elif request.method == "POST":
        pid = request.POST.get("id")
        pkg_name = request.POST.get("PkgName",None)
        project = request.POST.get("Project",None)
        pkg_path = request.POST.get("PkgPath",None)
        labels = request.POST.get("Labels",None)

        page = request.POST.get("page")

        form_data = {
            'PkgName':pkg_name,
            'Project':project,
            'PkgPath':pkg_path,
            'Labels':labels,
        }

        pkg_obj = ScriptPackage.objects.get(id=pid)
        try:
            for k ,v in form_data.items():
                setattr(pkg_obj,k,v)
                pkg_obj.save()
            result = {"code": 0, "message": "Package更新成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/package_list?status={0}&message={1}&page={2}'.
                            format(result.get("code", ""),
                                   result.get("message", ""),
                                   page))

def del_package(request):
    if request.method == "GET":
        pid = request.GET.get("pid")
        page = request.GET.get("page")
        try:
            ScriptPackage.objects.get(id=pid).delete()
            result = {"code": 0, "message": "Package删除成功!"}
        except Exception as e:
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/package_list?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page))

def script_list(request,pid):
    '''
    script列表
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
        package_obj = ScriptPackage.objects.get(id=pid)
        queryset = ScriptSrtInfo.objects.filter(Q(Q(SrtName__contains=search_q))
                                          ,PKGID=package_obj).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'monitor/script_list.html',locals())

def add_script(request):
    if request.method == "POST":
        pid = request.POST.get("pid")
        srt_name = request.POST.get("SrtName")
        git_repo = request.POST.get("GitRepo")
        git_branch = request.POST.get("GitBranch")
        git_commitid = request.POST.get("GitCommitID")
        page = request.POST.get("page")
        if srt_name:
            try:
                ScriptSrtInfo.objects.create(SrtName=srt_name,GitRepo=git_repo,GitBranch=git_branch
                                             ,GitCommitID=git_commitid,PKGID_id=pid)
                result = {"code": 0, "message": "Script创建成功!"}
            except Exception as e:
                result = {"code": 1, "message": str(e)}
        else:
            result = {"code": 1, "message": "必须指定名称!"}
        return HttpResponseRedirect('/monitor/script_list/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,pid))

def update_script(request):
    if request.method == "GET":
        sid = request.GET.get('sid',None)
        script_obj = ScriptSrtInfo.objects.filter(id=sid)
        s_dict = dict(script_obj.values('id','SrtName','GitRepo','GitBranch','GitCommitID').first())

        return HttpResponse(json.dumps(s_dict))

    elif request.method == "POST":
        pid = request.POST.get("pid")
        sid = request.POST.get("id")
        srt_name = request.POST.get("SrtName",None)
        git_repo = request.POST.get("GitRepo",None)
        git_branch = request.POST.get("GitBranch",None)
        git_commitid = request.POST.get("GitCommitID",None)

        page = request.POST.get("page")

        form_data = {
            'SrtName':srt_name,
            'GitRepo':git_repo,
            'GitBranch':git_branch,
            'GitCommitID':git_commitid,
        }

        srt_obj = ScriptSrtInfo.objects.get(id=sid)
        try:
            for k ,v in form_data.items():
                setattr(srt_obj,k,v)
                srt_obj.save()
            result = {"code": 0, "message": "Script更新成功！"}
        except Exception as e:
            print(traceback.format_exc())
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/script_list/{3}/?status={0}&message={1}&page={2}'.
                            format(result.get("code", ""),
                                   result.get("message", ""),
                                   page,pid))

def del_script(request):
    if request.method == "GET":
        pid = request.GET.get("pid")
        sid = request.GET.get("sid")
        page = request.GET.get("page")
        try:
            ScriptSrtInfo.objects.get(id=sid).delete()
            result = {"code": 0, "message": "Script删除成功!"}
        except Exception as e:
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/script_list/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,pid))

def fw_packages(request):
    '''
    fw包列表
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

        queryset = FWPackage.objects.filter(Q(Q(PkgName__contains=search_q) |
                                           Q(Project__contains=search_q) |
                                           Q(PkgType__contains=search_q) |
                                           Q(Labels__contains=search_q))
                                          ).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'monitor/fw_packages.html',locals())

def add_fwpkg(request):
    '''
    添加fw包
    :param request:
    :return:
    '''
    if request.method == "POST":
        pkg_name = request.POST.get("PkgName")
        project = request.POST.get("Project")
        external = request.POST.get("External")
        external = 1 if external == "on" else 0
        pkg_type = request.POST.get("PkgType")
        pkg_path = request.POST.get("PkgPath")
        page = request.POST.get("page")
        if pkg_name:
            try:
                FWPackage.objects.create(PkgName=pkg_name,Project=project,PkgPath=pkg_path,
                                         External=external,PkgType=pkg_type)
                result = {"code": 0, "message": "FWPackage创建成功!"}
            except Exception as e:
                result = {"code": 1, "message": str(e)}
        else:
            result = {"code": 1, "message": "必须指定名称!"}
        return HttpResponseRedirect('/monitor/fw_packages?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page))

def update_fwpkg(request):
    '''
    更新fw包
    :param request:
    :return:
    '''
    if request.method == "GET":
        pid = request.GET.get('pid',None)
        pkg_obj = FWPackage.objects.filter(id=pid)
        pkg_dict = pkg_obj.values('id','PkgName','Project','External',
                                  'PkgType','PkgPath','Labels').first()
        # print(pkg_dict)
        return HttpResponse(json.dumps(dict(pkg_dict)))

    elif request.method == "POST":
        pid = request.POST.get("id")
        pkg_name = request.POST.get("PkgName",None)
        project = request.POST.get("Project",None)
        external = request.POST.get("External",None)
        pkg_type = request.POST.get("PkgType",None)
        pkg_path = request.POST.get("PkgPath",None)
        labels = request.POST.get("Labels",None)

        page = request.POST.get("page")

        form_data = {
            'PkgName':pkg_name,
            'Project':project,
            'External':1 if external == 'on' else 0,
            'PkgType':pkg_type,
            'PkgPath':pkg_path,
            'Labels':labels,
        }

        pkg_obj = FWPackage.objects.get(id=pid)
        try:
            for k ,v in form_data.items():
                setattr(pkg_obj,k,v)
                pkg_obj.save()
            result = {"code": 0, "message": "FWPackage更新成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/fw_packages?status={0}&message={1}&page={2}'.
                            format(result.get("code", ""),
                                   result.get("message", ""),
                                   page))

def del_fwpkg(request):
    '''
    删除fw包
    :param request:
    :return:
    '''
    if request.method == "GET":
        pid = request.GET.get("pid")
        page = request.GET.get("page")
        try:
            FWPackage.objects.get(id=pid).delete()
            result = {"code": 0, "message": "FWPackage删除成功!"}
        except Exception as e:
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/fw_packages?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page))

def fw_binarys(request,pid):
    '''
    fw binarys列表
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
        package_obj = FWPackage.objects.get(id=pid)
        queryset = FWBinary.objects.filter(Q(Q(BinaryName__contains=search_q)|Q(BinaryType__contains=search_q))
                                          ,PKGID=package_obj).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'monitor/fw_binarys.html',locals())

def add_fwbin(request):
    '''
    添加fwbin
    :param request:
    :return:
    '''
    if request.method == "POST":
        pid = request.POST.get("pid")
        bin_name = request.POST.get("BinaryName")
        bin_type = request.POST.get("BinaryType")
        git_repo = request.POST.get("GitRepo")
        git_branch = request.POST.get("GitBranch")
        git_commitid = request.POST.get("GitCommitID")
        page = request.POST.get("page")
        if bin_name:
            try:
                FWBinary.objects.create(BinaryName=bin_name,BinaryType=bin_type,GitRepo=git_repo,
                                        GitBranch=git_branch,GitCommitID=git_commitid,PKGID_id=pid)
                result = {"code": 0, "message": "FWBinary创建成功!"}
            except Exception as e:
                result = {"code": 1, "message": str(e)}
        else:
            result = {"code": 1, "message": "必须指定名称!"}
        return HttpResponseRedirect('/monitor/fw_binarys/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,pid))

def update_fwbin(request):
    '''
    更新fwbin
    :param request:
    :return:
    '''
    if request.method == "GET":
        bid = request.GET.get('bid', None)
        bin_obj = FWBinary.objects.filter(id=bid)
        b_dict = dict(bin_obj.values('id', 'BinaryName', 'BinaryType', 'GitRepo',
                                     'GitBranch', 'GitCommitID').first())

        return HttpResponse(json.dumps(b_dict))

    elif request.method == "POST":
        pid = request.POST.get("pid")
        bid = request.POST.get("id")
        bin_name = request.POST.get("BinaryName", None)
        bin_type = request.POST.get("BinaryType", None)
        git_repo = request.POST.get("GitRepo", None)
        git_branch = request.POST.get("GitBranch", None)
        git_commitid = request.POST.get("GitCommitID", None)

        page = request.POST.get("page")

        form_data = {
            'BinaryName': bin_name,
            'BinaryType': bin_type,
            'GitRepo': git_repo,
            'GitBranch': git_branch,
            'GitCommitID': git_commitid,
        }

        bin_obj = FWBinary.objects.get(id=bid)
        try:
            for k, v in form_data.items():
                setattr(bin_obj, k, v)
                bin_obj.save()
            result = {"code": 0, "message": "FWBinary更新成功！"}
        except Exception as e:
            print(traceback.format_exc())
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/fw_binarys/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page, pid))

def del_fwbin(request):
    '''
    删除fwbin
    :param request:
    :return:
    '''
    if request.method == "GET":
        pid = request.GET.get("pid")
        bid = request.GET.get("bid")
        page = request.GET.get("page")
        try:
            FWBinary.objects.get(id=bid).delete()
            result = {"code": 0, "message": "FWBinary删除成功!"}
        except Exception as e:
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/fw_binarys/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,pid))

def fw_releases(request,pid):
    '''
    fw_release列表
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
        package_obj = FWPackage.objects.get(id=pid)
        queryset = FWRelease.objects.filter(Q(Q(Name__contains=search_q)|Q(TRName__contains=search_q)
                                              | Q(Version__contains=search_q))
                                          ,PKGID=package_obj).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'monitor/fw_releases.html',locals())

def add_fwrel(request):
    '''
    添加fwrel
    :param request:
    :return:
    '''
    if request.method == "POST":
        pid = request.POST.get("pid")
        tr_name = request.POST.get("TRName")
        rel_name = request.POST.get("Name")
        date = request.POST.get("Date")
        version = request.POST.get("Version")

        page = request.POST.get("page")
        if rel_name:
            try:
                FWRelease.objects.create(Name=rel_name,TRName=tr_name,Date=date,Version=version
                                         ,PKGID_id=pid)
                result = {"code": 0, "message": "FWRelease创建成功!"}
            except Exception as e:
                result = {"code": 1, "message": str(e)}
        else:
            result = {"code": 1, "message": "必须指定名称!"}
        return HttpResponseRedirect('/monitor/fw_releases/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,pid))

def update_fwrel(request):
    '''
    更新fwrel
    :param request:
    :return:
    '''
    if request.method == "GET":
        rid = request.GET.get('rid', None)
        rel_obj = FWRelease.objects.filter(id=rid)
        r_dict = dict(rel_obj.values('id', 'Name', 'TRName', 'Version').first())

        return HttpResponse(json.dumps(r_dict))

    elif request.method == "POST":
        pid = request.POST.get("pid")
        rid = request.POST.get("id")
        rel_name = request.POST.get("Name", None)
        tr_name = request.POST.get("TRName", None)
        version = request.POST.get("Version", None)

        page = request.POST.get("page")

        form_data = {
            'Name': rel_name,
            'TRName': tr_name,
            'Version': version,
        }

        rel_obj = FWRelease.objects.get(id=rid)
        try:
            for k, v in form_data.items():
                setattr(rel_obj, k, v)
                rel_obj.save()
            result = {"code": 0, "message": "FWRelease更新成功！"}
        except Exception as e:
            print(traceback.format_exc())
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/fw_releases/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page, pid))

def del_fwrel(request):
    '''
    删除fwrel
    :param request:
    :return:
    '''
    if request.method == "GET":
        pid = request.GET.get("pid")
        rid = request.GET.get("rid")
        page = request.GET.get("page")
        try:
            FWRelease.objects.get(id=rid).delete()
            result = {"code": 0, "message": "FWRelease删除成功!"}
        except Exception as e:
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/monitor/fw_releases/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,pid))