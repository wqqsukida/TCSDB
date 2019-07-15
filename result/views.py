from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import json
import copy
import traceback
import datetime
from utils.pagination import Pagination
from result.models import *
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

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

def func_res(request):
    '''
    func test 任务结果列表
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

        queryset = ResultSummary.objects.filter(TRName__contains=search_q).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'result/func_res.html',locals())

@csrf_exempt
def func_cases(request,rsid):

    if request.method == "GET":
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        rsid = rsid
        rs_obj = ResultSummary.objects.get(id=rsid)
        if status.isdigit():
            result = {"code": int(status), "message": message}
        return render(request, 'result/func_cases.html', locals())

    elif request.method == "POST":
        query_set = ResultDetail.objects.filter(TRID_id=rsid)
        rep = []
        for q in query_set:
            q_dict = {"id":q.id,"TCName": q.TCName, "Result": q.Result, "SerialNum": q.SerialNum,
                      "ScriptLog": q.ScriptLog, "FWLog": q.FWLog}
            if q.StartTime: q_dict["StartTime"] = q.StartTime.strftime('%Y-%m-%d %H:%m:%s')
            if q.EndTime: q_dict["EndTime"] = q.EndTime.strftime('%Y-%m-%d %H:%m:%s')
            rep.append(q_dict)
        return HttpResponse(json.dumps(rep))

def func_failure(request):
    if request.method == "GET":
        id = request.GET.get("cid")
        query_set = ResultFailure.objects.filter(RRID_id=id)
        rep = [model_to_dict(q) for q in query_set]

        return HttpResponse(json.dumps(rep))