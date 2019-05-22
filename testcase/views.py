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

def test_cases(request):
    '''
    主机列表
    :param request:
    :return:
    '''
    return render(request,'testcase/test_cases.html')

def GetProject(request, projectname):
    """
    """
    
    print("request is:%s" % request)
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
    """
    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        search_q = request.GET.get('q', '').strip()
        spec_list = ReferSpec.objects.filter(FileName__contains=search_q)
        queryset, page_html = init_paginaion(request, spec_list)
        return render(request,'testcase/test_specs.html',locals())

def AddRefSpec(request):
    """
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
                referspec = ReferSpec.objects.all()
                for spec in specList:
                    spec_obj.SpecAndPoint.add(referspec[int(spec)-1])
            result = {"code": 0, "message": "创建协议成功"}
        except Exception as e:
            result = {"code": 1, "message": e}
            print(e)

        return HttpResponseRedirect('/testcase/test_points?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                    result.get("message", "")))

def UpdateTestPoint(request):
    """
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