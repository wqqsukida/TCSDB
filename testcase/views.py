from django.shortcuts import render,HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
import json
import copy
from utils.pagination import Pagination
from django.db import transaction
from testcase.models import *
from asyncio.test_utils import TestCase

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

def GetProject(request, projectname):
    """
    获取项目的用例信息
    """
    #print("request is:%s" % dir(request))
    case_template = 'testcase/test_project.html'
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_case = request.GET.get('casename', '').strip()
        case_status = request.GET.get('searchstatus', '').strip()
        filter_dic = {}
        if search_case != "":
            filter_dic["TID__ScriptName__icontains"] = search_case
        #add project filter
        filter_dic["Project"] = projectname.replace('\'', '')
        #add filter status
        filter_dic["Status__icontains"] = case_status
        print("filter dic:%s" % filter_dic)
        case_list = TestProject.objects.filter(**filter_dic).distinct()
        queryset, page_html = init_paginaion(request, case_list)
        return render(request,case_template,locals())

def AddProject(request, projectname):
    """
    添加项目的用例信息
    """
    result = {}
    print("project name:%s" %projectname)
    if request.method == "POST":
        pjname = request.POST.get("pjname",None)
        caseid = request.POST.get("caseid",None)
        casestatus = request.POST.get("casestatus",None)
        meet_condition = True
        #check input prject name
        if pjname != projectname:
            result = {"code": 1, "message": "should input correct project name"}
            meet_condition = False
        print(pjname,caseid,casestatus)
        #check input case id
        case_all = TestCaseDetail.objects.all()
        case_list = [x.id for x in case_all]
        print("case_list:%s" % case_list)
        if int(caseid) not in case_list:
            meet_condition = False
            result = {"code": 1, "message": "should input correct case id"}
        #check input case status
        status_all = TestProject.StatusChoice
        status_list = [x[0] for x in status_all]
        if casestatus.upper() not in status_list:
            meet_condition = False
            result = {"code": 1, "message": "should input correct case id"}
        if meet_condition == True:
            try:
                with transaction.atomic():
                    pj_obj = TestProject(Project=pjname, Status=casestatus.upper())
                    pj_obj.save()
                    test_case = TestCaseDetail.objects.get(pk=int(caseid))
                    pj_obj.TID.add(test_case)
    
                result = {"code": 0, "message": "创建用例成功"}
            except Exception as e:
                result = {"code": 1, "message": e}
                print(e)

        return HttpResponseRedirect('/testcase/test_project/'+projectname+'/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdateProject(request, projectname):
    """
    更新项目的用例信息
    """
    if request.method == "GET":
        res = {}
        id = request.GET.get("id",None)
        project_obj = TestProject.objects.filter(id=id)
        case_dict = project_obj.values().first()
        if case_dict:
            cases = project_obj.first().TID.all()
            case_list = [pt.id for pt in cases]
            case_dict['TID'] = case_list
            res = dict(case_dict)
        print("case_dict:%s" %case_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result = {}
        pjid = request.POST.get("id")
        projectname = request.POST.get("projectname",None)
        caseid = request.POST.get("caseid",None)
        casestatus = request.POST.get("casestatus",None).upper()
        print("case status:%s" % casestatus)
        form_data = {
                    'id'     :pjid,
                    'Project':projectname,
                    'Status' :casestatus,
                    'TID'    :caseid, 
        }
        pj_obj = TestProject.objects.get(id=pjid)
        try:
            for k ,v in form_data.items():
                if k == "TID":
                    pj_obj.TID.set(v)
                else:
                    setattr(pj_obj,k,v)
            pj_obj.save()
            result = {"code": 0, "message": "更新协议成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/testcase/test_project/'+projectname+'/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def GetTestCase(request):
    """
    获取功能测试用例
    """
    case_template = 'testcase/test_cases.html'
    print("case request:%s" % dir(request))
    print("case local:%s" % locals())      
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_pt = request.GET.get('searchpt', '').strip()
        search_name = request.GET.get('searchname', '').strip()
        search_cate  = request.GET.get('searchcate', '').strip()
        filter_dic = {}
        print("search_cate is:%s, type is:%s" %(search_cate, type(search_cate)))
        if search_name != "":
            filter_dic["ScriptName"] = search_name
        if search_cate != "":
            filter_dic["Category"] = search_cate
        if search_pt != "":
            pt_list = search_pt.split(",")
            print("point list:%s" % pt_list)
            filter_dic["CaseAndPoint__id__in"] = pt_list
        print("filter dic:%s" % filter_dic)
        case_list = TestCaseDetail.objects.filter(**filter_dic).distinct()
        test_points = TestPoint.objects.all()
        queryset, page_html = init_paginaion(request, case_list)
        print("local:%s" % locals())
        return render(request,case_template,locals())

def AddTestCase(request):
    """
    添加功能测试用例
    """
    result = {}
    if request.method == "POST":
        casename= request.POST.get("casename",None)
        casedesc= request.POST.get("casedesc",None)
        scriptname= request.POST.get("scriptname",None)
        scriptpath= request.POST.get("scriptpath",None)
        scriptparams= request.POST.get("scriptparams",None)
        scriptversion= request.POST.get("scriptversion",None)
        caseauthor= request.POST.get("caseauthor",None)
        caseowner= request.POST.get("caseowner",None)
        casebkowner= request.POST.get("casebkowner",None)
        caseauto= request.POST.get("caseauto",None)
        scriptratio= request.POST.get("scriptratio",None)
        scriptlevel= request.POST.get("scriptlevel",None)
        scriptcate= request.POST.get("scriptcate",None)
        scriptsubcate= request.POST.get("scriptsubcate",None)
        scriptlabel= request.POST.get("scriptlabel",None)
        casehw= request.POST.get("casehw",None)
        casesw= request.POST.get("casesw",None)
        casevs= request.POST.get("casevs",None)
        casedrv= request.POST.get("casedrv",None)
        caseos= request.POST.get("caseos",None)
        caseoem= request.POST.get("caseoem",None)
        casesku= request.POST.get("casesku",None)
        pointids= request.POST.get("pointid",None)
        print("casename:%s, casedesc:%s,scriptname:%s, scriptpath:%s,scriptparams:%s"
              %(casename, casedesc, scriptname, scriptpath, scriptparams))
        print("scriptversion:%s, caseauthor:%s,caseowner:%s, casebkowner:%s,caseauto:%s"
              %(scriptversion, caseauthor, caseowner, casebkowner, caseauto))
        print("scriptratio:%s, scriptlevel:%s,scriptcate:%s, scriptsubcate:%s,scriptlabel:%s,casehw:%s"
              %(scriptratio, scriptlevel, scriptcate, scriptsubcate, scriptlabel, casehw))
        print("casesw:%s, casevs:%s,casedrv:%s, caseos:%s,caseoem:%s, casesku:%s"
              %(casesw, casevs, casedrv, caseos, caseoem, casesku))

        try:
            with transaction.atomic():
                case_obj = TestCaseDetail(CaseName=casename, Description=casedesc, ScriptName=scriptname, ScriptPath=scriptpath, ScriptParams=scriptparams,
                                          Version=scriptversion, Author=caseauthor, Owner=caseowner, BackupOwner=casebkowner, Automated=caseauto, Importance=scriptratio,
                                          Level=scriptlevel, Category=scriptcate, Subcategory=scriptsubcate, Labels=scriptlabel, HWRequired=casehw, SWRequired=casesw,
                                          VSRequired=casevs,DrvSupported=casedrv, OSSupported=caseos, OEMSupported=caseoem, SKUSupported=casesku)
                case_obj.save()
                pointList = pointids.split(",")
                print("pointList is:%s" % pointList)
                pointobjs = TestPoint.objects.all()
                for pt in pointList:
                    case_obj.CaseAndPoint.add(pointobjs[int(pt)-1])
            result = {"code": 0, "message": "创建测试用例成功"}
        except Exception as e:
            result = {"code": 1, "message": e}
            print(e)

        return HttpResponseRedirect('/testcase/test_cases?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdateTestCase(request):
    """
    更新功能测试用例
    """
    if request.method == "GET":
        res = {}
        id = request.GET.get("id",None)
        case_obj = TestCaseDetail.objects.filter(id=id)
        case_dict = case_obj.values().first()
        if case_dict:
            cases = case_obj.first().CaseAndPoint.all()
            point_list = [pt.id for pt in cases]
            case_dict['CaseAndPoint'] = point_list
            res = dict(case_dict)
        print("case_dict:%s" %case_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result = {}
        caseid = request.POST.get("id")
        casename= request.POST.get("casename",None)
        casedesc= request.POST.get("casedesc",None)
        scriptname= request.POST.get("scriptname",None)
        scriptpath= request.POST.get("scriptpath",None)
        scriptparams= request.POST.get("scriptparams",None)
        scriptversion= request.POST.get("scriptversion",None)
        caseauthor= request.POST.get("caseauthor",None)
        caseowner= request.POST.get("caseowner",None)
        casebkowner= request.POST.get("casebkowner",None)
        caseauto= request.POST.get("caseauto",None)
        scriptratio= request.POST.get("scriptratio",None)
        scriptlevel= request.POST.get("scriptlevel",None)
        scriptcate= request.POST.get("scriptcate",None)
        scriptsubcate= request.POST.get("scriptsubcate",None)
        scriptlabel= request.POST.get("scriptlabel",None)
        casehw= request.POST.get("casehw",None)
        casesw= request.POST.get("casesw",None)
        casevs= request.POST.get("casevs",None)
        casedrv= request.POST.get("casedrv",None)
        caseos= request.POST.get("caseos",None)
        caseoem= request.POST.get("caseoem",None)
        casesku= request.POST.get("casesku",None)
        pointids= request.POST.getlist("pointid",None)
        print("pointids :%s" % pointids)
        form_data = {
            'id'           :caseid,
            'CaseName'     :casename,
            'Description'  :casedesc,
            'ScriptName'   :scriptname,
            'ScriptPath'   :scriptpath,
            'ScriptParams' :scriptparams,
            'Version'      :scriptversion,
            'Author'       :caseauthor,
            'Owner'        :caseowner,
            'BackupOwner'  :casebkowner,
            'Automated'    :caseauto,
            'Importance'   :scriptratio,
            'Level'        :scriptlevel,
            'Category'     :scriptcate,
            'Subcategory'  :scriptsubcate,
            'Labels'       :scriptlabel,
            'HWRequired'   :casehw,
            'SWRequired'   :casesw,
            'VSRequired'   :casevs,
            'DrvSupported' :casedrv,
            'OSSupported'  :caseos,
            'OEMSupported' :caseoem,
            'SKUSupported' :casesku,
            'CaseAndPoint' :pointids,
        }
        case_obj = TestCaseDetail.objects.get(id=caseid)
        try:
            for k ,v in form_data.items():
                if k == "CaseAndPoint":
                    case_obj.CaseAndPoint.set(v)
                else:
                    setattr(case_obj,k,v)
            case_obj.save()
            result = {"code": 0, "message": "更新用例成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/testcase/test_cases?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def DeleteTestCase(request):
    """
    删除功能测试用例
    """
    if request.method == "GET":
        pointid =request.GET.get("id",None)
        try:
            with transaction.atomic():
                TestPoint.objects.filter(id=pointid).delete()
                result = {"code": 0, "message": "删除用例成功！"}
        except Exception as e:
            result = {"code": 1, "message":e }

        return HttpResponseRedirect('/testcase/test_cases?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                   result.get("message", "")))

def GetTestStep(request):
    """
    获取功能测试用例步骤
    """
    case_template = 'testcase/test_steps.html'
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        case_id = request.GET.get('id', '')
        print("case id:%s" % case_id)
        case_obj = TestCaseDetail.objects.filter(id=case_id)
        print("case obj :%s" % case_obj)
        step_list = case_obj.first().case_step.all()
        print("step_list:%s" % step_list)
        queryset, page_html = init_paginaion(request, step_list)
        print("queryset:%s" %queryset)
        return render(request,case_template,locals())

def GetRefSpec(request):
    """
    获取参考协议信息
    """
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_q = request.GET.get('q', '').strip()
        spec_list = ReferSpec.objects.filter(FileName__contains=search_q).order_by('id')
        queryset, page_html = init_paginaion(request, spec_list)
        return render(request,'testcase/test_specs.html',locals())

def AddRefSpec(request):
    """
    添加参考协议信息
    """
    result = {}
    if request.method == "POST":
        specname = request.POST.get("specname",None)
        referstd = request.POST.get("stdspec",None)
        specver = request.POST.get("specver",None)
        specpath = request.POST.get("specpath",None)

        print(specname,referstd,specver,specpath)

        try:
            with transaction.atomic():
                spec_obj = ReferSpec(FileName=specname, Standard=referstd, 
                                    Version=specver, FilePath=specpath)
                spec_obj.save()

            result = {"code": 0, "message": "创建协议成功"}
        except Exception as e:
            result = {"code": 1, "message": e}
            print(e)

        return HttpResponseRedirect('/testcase/test_specs?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdateRefSpec(request):
    """
    更新参考协议信息
    """
    if request.method == "GET":
        res = {}
        id = request.GET.get("id",None)
        spec_obj = ReferSpec.objects.filter(id=id)
        spec_dict = spec_obj.values().first()
        if spec_dict:
            res = dict(spec_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result = {}
        specid = request.POST.get("id")
        specname = request.POST.get("specname",None)
        referstd = request.POST.get("stdspec",None)
        specver = request.POST.get("specver",None)
        specpath = request.POST.get("specpath",None)

        form_data = {
            'id':specid,
            'FileName':specname,
            'Standard':referstd,
            'Version':specver,
            'FilePath':specpath,
        }
        spec_obj = ReferSpec.objects.get(id=specid)
        try:
            for k ,v in form_data.items():
                setattr(spec_obj,k,v)
            spec_obj.save()
            result = {"code": 0, "message": "更新协议成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/testcase/test_specs?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))
def DeleteRefSpec(request):
    """
    删除参考协议信息
    """
    if request.method == "GET":
        specid =request.GET.get("id",None)
        try:
            with transaction.atomic():
                ReferSpec.objects.filter(id=specid).delete()
                result = {"code": 0, "message": "删除协议成功！"}
        except Exception as e:
            result = {"code": 1, "message":e }

        return HttpResponseRedirect('/testcase/test_specs?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                   result.get("message", "")))

def GetTestPoint(request):
    """
    获取测试点信息
    """
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_tp = request.GET.get('tp', '').strip()
        search_spec_name = request.GET.get('spec', '').strip()
        search_spec_ver  = request.GET.get('specver', '').strip()
        #only search test point information
        filter_dic = {}
        if search_tp != "":
            filter_dic["id"] = int(search_tp)
        if search_spec_name != "":
            specList = ReferSpec.objects.filter(FileName=search_spec_name).distinct()
            specList = [x.id for x in specList]
            filter_dic["SpecAndPoint__id__in"] = specList
        if search_spec_ver != "":
            verList = ReferSpec.objects.filter(Version=search_spec_ver).distinct()
            verList = [x.Version for x in verList]
            filter_dic["SpecAndPoint__Version__in"] = verList
        point_list = TestPoint.objects.filter(**filter_dic).distinct()
        referspec = ReferSpec.objects.all()
        queryset, page_html = init_paginaion(request, point_list)
        return render(request,'testcase/test_points.html',locals())

def AddTestPoint(request):
    """
     添加测试点信息
    """
    result = {}
    if request.method == "POST":
        pointdes = request.POST.get("pointdesc",None)
        pointfrom = request.POST.get("pointfrom",None)
        pointpage = request.POST.get("pointpage",None)
        pointspec = request.POST.get("specid", None)
        print("pointspec is:%s" % pointspec)
        print(pointdes,pointfrom,pointpage)

        try:
            with transaction.atomic():
                spec_obj = TestPoint(TestDesc=pointdes, SelectFrom=pointfrom, PageNo=pointpage)
                spec_obj.save()
                specList = pointspec.split(",")
                print("specList is:%s" % specList)
                spec_obj.SpecAndPoint.set(specList)
#                 referspec = ReferSpec.objects.all()
#                 for spec in specList:
#                     spec_obj.SpecAndPoint.add(referspec[int(spec)-1])
            result = {"code": 0, "message": "创建协议成功"}
        except Exception as e:
            result = {"code": 1, "message": e}
            print(e)

        return HttpResponseRedirect('/testcase/test_points?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdateTestPoint(request):
    """
     更新测试点信息
    """
    if request.method == "GET":
        res = {}
        id = request.GET.get("id",None)
        point_obj = TestPoint.objects.filter(id=id)
        point_dict = point_obj.values().first()
        if point_dict:
            specs = point_obj.first().SpecAndPoint.all()
            specid_list = [spec.id for spec in specs]
            point_dict['SpecAndPoint'] = specid_list
            res = dict(point_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result = {}
        pointid = request.POST.get("id")
        pointdesc = request.POST.get("pointdesc",None)
        pointfrom = request.POST.get("pointfrom",None)
        pointpage = request.POST.get("pointpage",None)
        specId = request.POST.getlist("specid",None)
        form_data = {
            'id':pointid,
            'TestDesc':pointdesc,
            'SelectFrom':pointfrom,
            'PageNo':pointpage,
            'SpecAndPoint':specId,
        }
        point_obj = TestPoint.objects.get(id=pointid)
        try:
            for k ,v in form_data.items():
                if k == "SpecAndPoint":
                    point_obj.SpecAndPoint.set(v)
                else:
                    setattr(point_obj,k,v)
            point_obj.save()
            result = {"code": 0, "message": "更新协议成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/testcase/test_points?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))
def DeleteTestPoint(request):
    """
     删除测试点信息
    """
    if request.method == "GET":
        pointid =request.GET.get("id",None)
        try:
            with transaction.atomic():
                TestPoint.objects.filter(id=pointid).delete()
                result = {"code": 0, "message": "删除协议成功！"}
        except Exception as e:
            result = {"code": 1, "message":e }

        return HttpResponseRedirect('/testcase/test_points?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                   result.get("message", "")))

def GetPerfGlobal(request):
    """
     获取新能测试的全局变量信息
    """
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_name = request.GET.get('sname', '').strip()
        search_content = request.GET.get('scontent', '').strip()
        filter_dic = {}
        name_dic = { "变量名称"      : "GlobalName",
                    "全局最大IOSize" : "MaxIOSize",
                    "偏移量"        : "Offset",
                    "是否需要Purge"  : "NeedPurge",
                    "是否需要2XFill Driver":"Need2XFillDriver"
                    }
        if search_name != "" and  search_content != "":
            filter_dic.update({name_dic[search_name]+"__icontains":search_content,})
        print("filter dic is:%s" % filter_dic)
        global_list = PerfGlobal.objects.filter(**filter_dic)
        queryset, page_html = init_paginaion(request, global_list)
        return render(request,'testcase/perf_get_global.html',locals())


def AddPerfGlobal(request):
    """
     新增全局测试信息
    """
    result = {}
    if request.method == "POST":
        perfName      = request.POST.get("globalname",None)
        perfMaxIo     = request.POST.get("maxio",None)
        perfOffset    = request.POST.get("offset",None)
        perfNeedPurge = request.POST.get("purge", None)
        perf2XFill    = request.POST.get("mfill", None)
        print("perfName is:%s" % perfName)
        print(perfMaxIo,perfOffset,perfNeedPurge,perf2XFill)
        try:
            with transaction.atomic():
                global_obj = PerfGlobal(GlobalName=perfName, MaxIOSize=perfMaxIo, Offset=perfOffset,
                                        NeedPurge=perfNeedPurge, Need2XFillDriver=perf2XFill)
                global_obj.save()
            result = {"code": 0, "message": "新增Perf全局信息成功"}
        except Exception as e:
            result = {"code": 1, "message": e}
            print(e)

        return HttpResponseRedirect('/testcase/perf_get_global?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdatePerfGlobal(request):
    """
    修改全局测试信息
    """
    if request.method == "GET":
        res = {}
        id = request.GET.get("id",None)
        global_obj = PerfGlobal.objects.filter(id=id)
        global_dict = global_obj.values().first()
        if global_dict:
            res = dict(global_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result        = {}
        perfId        = request.POST.get("id")
        perfName      = request.POST.get("globalname",None)
        perfMaxIo     = request.POST.get("maxio",None)
        perfOffset    = request.POST.get("offset",None)
        perfNeedPurge = request.POST.get("purge", None)
        perf2XFill    = request.POST.get("mfill", None)
        form_data = {
                    'id'        :perfId,
                    'GlobalName':perfName,
                    'MaxIOSize' :perfMaxIo,
                    'Offset'     :perfOffset,
                    'NeedPurge'  :perfNeedPurge,
                    'Need2XFillDriver':perf2XFill
                    }
        try:
            global_obj = PerfGlobal.objects.filter(id=perfId).first()
            for k ,v in form_data.items():
                setattr(global_obj,k,v)
            global_obj.save()
            result = {"code": 0, "message": "更新Perf全局变量成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/testcase/perf_get_global?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))
def DeletePerfGlobal(request):
    """
    删除全局测试信息
    """
    if request.method == "GET":
        globalId =request.GET.get("id",None)
        try:
            with transaction.atomic():
                PerfGlobal.objects.filter(id=globalId).delete()
                result = {"code": 0, "message": "删除Perf全局变量成功！"}
        except Exception as e:
            result = {"code": 1, "message":e }

        return HttpResponseRedirect('/testcase/perf_get_global?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                   result.get("message", "")))

def GetPerfTestItem(request):
    """
    获取测试项目的信息
    """
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_name = request.GET.get('sname', '').strip()
        search_content = request.GET.get('scontent', '').strip()
        filter_dic = {}
        name_dic = { "条目名称"            : "ItemName",
                    "测试点"               : "CheckPoint",
                    "可访问区间百分比"        : "AccessPercent",
                    "数据传输块大小(byte)"   : "BlockSize",
                    "数据块对齐大小(byte)"   :"BlockAlign",
                    "IO命令深度"           :"IODepth",
                    "Read占百分比"         :"RWMixRead",
                    "随机百分比"            :"RandPercent",
                    "并行Job的数目"         :"NumJobs",
                    "测试执行时间(单位：秒)"   :"RunTime",
                    "测试开始前的静默时间(单位：秒)" :"StartDelay",
                    "循环执行次数"           :"LoopCnt",
                    }
        if search_name != "" and  search_content != "":
            filter_dic.update({name_dic[search_name]+"__icontains":search_content,})
        print("filter dic is:%s" % filter_dic)
        item_list = PerfTestItem.objects.filter(**filter_dic)
        queryset, page_html = init_paginaion(request, item_list)
        return render(request,'testcase/perf_get_item.html',locals())

def AddPerfTestItem(request):
    """
    添加测试项目的信息
    """
    result = {}
    if request.method == "POST":
        itemName  = request.POST.get("itemname",None)
        checkPoint = request.POST.get("checkpoint",None)
        accessPercent = request.POST.get("accesspercent",None)
        blkSize = request.POST.get("blksize", None)
        blkAlign = request.POST.get("blkalign", None)
        ioDepth = request.POST.get("iodepth", None)
        rwMixRead = request.POST.get("rwmixread", None)
        randPercent = request.POST.get("randpercent", None)
        numJobs = request.POST.get("numjobs", None)
        runTime = request.POST.get("runtime", None)
        strDelay = request.POST.get("strdelay", None)
        loopCnt  = request.POST.get("loopcnt", None)
        print("variable is:%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s" 
              %(itemName,checkPoint,accessPercent, blkSize, blkAlign, ioDepth, rwMixRead,
                randPercent, numJobs, runTime, strDelay, loopCnt))
        try:
            with transaction.atomic():
                item_obj = PerfTestItem(ItemName=itemName, CheckPoint=checkPoint, AccessPercent=accessPercent, BlockSize=blkSize,
                                        BlockAlign=blkAlign, IODepth=ioDepth, RWMixRead=rwMixRead, RandPercent=randPercent,
                                        NumJobs=numJobs, RunTime=runTime, StartDelay=strDelay, LoopCnt=loopCnt)
                item_obj.save()
            result = {"code": 0, "message": "创建Perf项目成功"}
        except Exception as e:
            result = {"code": 1, "message": e}
            print(e)

        return HttpResponseRedirect('/testcase/perf_get_item?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdatePerfTestItem(request):
    """
    更新测试项目的信息
    """
    if request.method == "GET":
        res = {}
        id = request.GET.get("id",None)
        item_obj = PerfTestItem.objects.filter(id=id)
        item_dict = item_obj.values().first()
        if item_dict:
            res = dict(item_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result = {}
        itemId = request.POST.get("id")
        itemName  = request.POST.get("itemname",None)
        checkPoint = request.POST.get("checkpoint",None)
        accessPercent = request.POST.get("accesspercent",None)
        blkSize = request.POST.get("blksize", None)
        blkAlign = request.POST.get("blkalign", None)
        ioDepth = request.POST.get("iodepth", None)
        rwMixRead = request.POST.get("rwmixread", None)
        randPercent = request.POST.get("randpercent", None)
        numJobs = request.POST.get("numjobs", None)
        runTime = request.POST.get("runtime", None)
        strDelay = request.POST.get("strdelay", None)
        loopCnt  = request.POST.get("loopcnt", None)
        form_data = {
            'id'      :itemId,
            'ItemName':itemName,
            'CheckPoint':checkPoint,
            'AccessPercent':accessPercent,
            'BlockSize':blkSize,
            'BlockAlign':blkAlign,
            'IODepth':ioDepth,
            'RWMixRead':rwMixRead,
            'RandPercent':randPercent,
            'NumJobs':numJobs,
            'RunTime':runTime,
            'StartDelay':strDelay,
            'LoopCnt':loopCnt,
        }
        item_obj = PerfTestItem.objects.get(id=itemId)
        try:
            for k ,v in form_data.items():
                setattr(item_obj,k,v)
            item_obj.save()
            result = {"code": 0, "message": "更新Perf项目成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/testcase/perf_get_item?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))
def DeletePerfTestItem(request):
    """
    删除测试项目的信息
    """
    if request.method == "GET":
        pointid =request.GET.get("id",None)
        try:
            with transaction.atomic():
                PerfTestItem.objects.filter(id=pointid).delete()
                result = {"code": 0, "message": "删除Perf项目成功！"}
        except Exception as e:
            result = {"code": 1, "message":e }

        return HttpResponseRedirect('/testcase/perf_get_item?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                   result.get("message", "")))

def GetPerfTestCase(request):
    """
    获取性能测试用例信息
    """
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_case_name = request.GET.get('scase', '').strip()
        search_case_level = request.GET.get('slevel', '').strip()
        search_case_type  = request.GET.get('stype', '').strip()
        #only search test point information
        filter_dic = {}
        if search_case_name != "":
            filter_dic["CaseName__icontains"] = search_case_name
        if search_case_level != "":
            filter_dic["Level__icontains"] = search_case_level
        if search_case_type != "":
            filter_dic["CaseType__icontains"] = search_case_type
        case_list = PerfTestCase.objects.filter(**filter_dic).distinct()
        global_obj = PerfGlobal.objects.all()
        queryset, page_html = init_paginaion(request, case_list)
        return render(request,'testcase/perf_get_case.html',locals())

def AddPerfTestCase(request):
    """
    新增性能测试用例信息
    """
    result = {}
    if request.method == "POST":
        caseName= request.POST.get("casename",None)
        caseLevel = request.POST.get("caselevel",None)
        caseType = request.POST.get("casetype",None)
        caseInitId = request.POST.get("caseinitid", None)
        print("variable is:%s, %s, %s, %s" %
              (caseName,caseLevel,caseType, caseInitId))

        try:
            with transaction.atomic():
                init_obj = PerfGlobal.objects.get(id=caseInitId)
                case_obj = PerfTestCase(CaseName=caseName, Level=caseLevel, CaseType=caseType, TIID=init_obj)
                case_obj.save()
                result = {"code": 0, "message": "创建Perf用例成功"}
        except Exception as e:
            result = {"code": 1, "message": e}
            print(e)

        return HttpResponseRedirect('/testcase/perf_get_case?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdatePerfTestCase(request):
    """
    更新性能测试用例信息
    """
    if request.method == "GET":
        res = {}
        id = request.GET.get("id",None)
        case_obj = PerfTestCase.objects.filter(id=id)
        case_dict = case_obj.values().first()
        if case_dict:
            res = dict(case_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result = {}
        caseid = request.POST.get("id")
        caseName= request.POST.get("casename",None)
        caseLevel = request.POST.get("caselevel",None)
        caseType = request.POST.get("casetype",None)
        caseInitId = request.POST.get("caseinitid", None)
        form_data = {
                    'id'      :caseid,
                    'CaseName':caseName,
                    'Level'   :caseLevel,
                    'CaseType':caseType,
                    'TIID'    :caseInitId,
                    }
        case_obj = PerfTestCase.objects.get(id=caseid)
        g_obj = PerfGlobal.objects.get(pk=caseInitId)
        try:
            for k ,v in form_data.items():
                if k == "TIID":
                    setattr(case_obj, k, g_obj)
                else:
                    setattr(case_obj,k,v)
            case_obj.save()
            result = {"code": 0, "message": "更新Perf用例成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/testcase/perf_get_case?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))
def DeletePerfTestCase(request):
    """
    删除性能测试用例信息
    """
    if request.method == "GET":
        caseId =request.GET.get("id",None)
        try:
            with transaction.atomic():
                PerfTestCase.objects.filter(id=caseId).delete()
                result = {"code": 0, "message": "删除Perf用例成功！"}
        except Exception as e:
            result = {"code": 1, "message":e }

        return HttpResponseRedirect('/testcase/perf_get_case?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                   result.get("message", "")))

def GetPerfCaseInfo(request):
    """
    获取项目性能测试用例信息
    """
    case_template = 'testcase/perf_get_case_info.html'
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        case_id = request.GET.get('id', '')
        print("case id:%s" % case_id)
        case_obj = PerfItemInCase.objects.filter(TCID__id=case_id)
        refer_obj = PerfRefTarget.objects.filter(IICID__TCID__id=case_id)
        print("case obj :%s" % case_obj)
        print("refer obj:%s" % refer_obj)
        queryset, page_html = init_paginaion(request, case_obj)
        print("queryset:%s" %queryset)
        return render(request,case_template,locals())

def GetPerfProject(request, projectName):
    """
    获取项目性能测试用例信息
    """
    case_template = 'testcase/perf_test_project.html'
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_case = request.GET.get('casename', '').strip()
        search_level = request.GET.get('searchlevel', '').strip()
        filter_dic = {}
        if search_case != "":
            filter_dic["IICID__TCID__CaseName__icontains"] = search_case
        if search_level !="":
            filter_dic["IICID__TCID__Level__icontains"] = search_level
        #add project filter
        filter_dic["Project"] = projectName.replace('\'', '')
        print("filter dic:%s" % filter_dic)
        case_list = PerfRefTarget.objects.filter(**filter_dic).distinct()
        item_case_list = PerfItemInCase.objects.all()
        queryset, page_html = init_paginaion(request, case_list)
        return render(request,case_template,locals())

def AddPerfProject(request, projectName):
    """
    新增项目性能测试用例信息
    """
    result = {}
    print("project name:%s" %projectName)
    if request.method == "GET":
        res = {}
        project_obj = PerfRefTarget.objects.all()
        project_dict = project_obj.values().first()
        if project_dict:
            res = dict(project_dict)
        print("case_dict:%s" %project_dict)
        return HttpResponse(json.dumps(res))
    elif request.method == "POST":
        pjName = request.POST.get("pjname",None)
        refUnit = request.POST.get("refunit",None)
        refVal = request.POST.get("refval",None)
        itemCaseId = request.POST.get("iicid",None)
        #check pjname
        if pjName != projectName:
            result = {"code": 1, "message": "project name error"}
        else:
            #check input case id
            try:
                getItemCaseObj = PerfItemInCase.objects.get(pk=itemCaseId)
                try:
                    with transaction.atomic():
                        pj_obj = PerfRefTarget(Project=pjName, RefUnit=refUnit.upper(), RefVal=refVal, IICID=getItemCaseObj)
                        pj_obj.save()   
                    result = {"code": 0, "message": "创建用例成功"}
                except Exception as e:
                    result = {"code": 1, "message": e}
                    print(e)
            except Exception as e:
                result = {"code": 1, "message": e}
                print(e)
        print("project name2:%s" % projectName)
        return HttpResponseRedirect('/testcase/perf_test_project/'+projectName+'/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdatePerfProject(request, projectName):
    """
    更新项目性能测试用例信息
    """
    if request.method == "GET":
        res = {}
        id = request.GET.get("id",None)
        project_obj = PerfRefTarget.objects.filter(id=id)
        case_dict = project_obj.values().first()
        if case_dict:
            res = dict(case_dict)
        print("case_dict:%s" %case_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result = {}
        pjid = request.POST.get("id")
        pjName = request.POST.get("pjname",None)
        refUnit = request.POST.get("refunit",None)
        refVal = request.POST.get("refval",None)
        itemCaseId = request.POST.get("iicid",None)
        form_data = {
                    'id'     :pjid,
                    'Project':pjName,
                    'RefUnit' :refUnit,
                    'RefVal'  :refVal,
                    'IICID'   :itemCaseId
        }
        pj_obj = PerfRefTarget.objects.get(id=pjid)
        try:
            for k ,v in form_data.items():
                if k == "IICID":
                    ii_obj = PerfItemInCase.objects.get(pk=itemCaseId)
                    setattr(pj_obj, k, ii_obj)
                else:
                    setattr(pj_obj,k,v)
            pj_obj.save()
            result = {"code": 0, "message": "更新协议成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/testcase/perf_test_project/'+pjName+'/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))
