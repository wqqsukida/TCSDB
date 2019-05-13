from django.shortcuts import render,HttpResponse, HttpResponseRedirect, get_object_or_404
from utils.auth_token import APIAuthView
from django.utils.decorators import method_decorator
from django.views import View
import json
import copy
from utils.pagination import Pagination
from django.db import transaction
from testcase.models import *

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

def api_list(request):
    return HttpResponse("api_list")

class ApiList(APIAuthView):
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(response)

    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'success!','data':{}}

        return HttpResponse(json.dumps(response))


def test_cases(request):
    '''
    主机列表
    :param request:
    :return:
    '''
    return render(request,'testcase/test_cases.html')

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
            filter_dic['TPID'] = TestPoint.objects.filter(id=int(search_tp))
            print(filter_dic)
        if search_spec_name != "":
            filter_dic['SpecID'] = ReferSpec.objects.filter(FileName=search_spec_name)
        if search_spec_ver != "":
            filter_dic['Version'] = ReferSpec.objects.filter(Version=search_spec_ver)
        if len(filter_dic) > 0:
            point_list = TestPoint.objects.filter(**filter_dic)
        else:
            point_list = TestPoint.objects.all()
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

        print(pointdes,pointfrom,pointpage)

        try:
            with transaction.atomic():
                spec_obj = TestPoint(TestDesc=pointdes, SelectFrom=pointfrom, PageNo=pointpage)
                spec_obj.save()

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
            res = dict(point_dict)
        return HttpResponse(json.dumps(res))

    elif request.method == "POST":
        result = {}
        pointid = request.POST.get("id")
        pointdesc = request.POST.get("pointdesc",None)
        pointfrom = request.POST.get("pointfrom",None)
        pointpage = request.POST.get("pointpage",None)

        form_data = {
            'id':pointid,
            'TestDesc':pointdesc,
            'SelectFrom':pointfrom,
            'PageNo':pointpage,
        }
        point_obj = TestPoint.objects.get(id=pointid)
        try:
            for k ,v in form_data.items():
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

def test_detail_cases(request):
    """
    """
    pass

def oc_test_cases(request):
    """
    """
    pass

def taiplus_test_cases(request):
    """
    """
    pass

def oc_perf_test_cases(request):
    """
    """
    pass

def taiplus_perf_test_cases(request):
    """
    """
    pass

def test_perf_detail_cases(request):
    """
    """
    pass

def oc_com_test_cases(request):
    """
    """
    pass

def taiplus_com_test_cases(request):
    """
    """
    pass

def test_com_detail_cases(request):
    """
    """
    pass
