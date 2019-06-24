from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import json
import copy
import traceback
import datetime
from utils.pagination import Pagination
from cccs.models import *
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

def test_cycles(request):
    '''
    test_cycle列表
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

        queryset = TestCycle.objects.filter(Q(Q(CycleName__contains=search_q) |
                                           Q(Project__contains=search_q) |
                                           Q(Status__contains=search_q) |
                                           Q(CycleLevel__contains=search_q))
                                          ).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'cccs/test_cycles.html',locals())

def add_test_cycle(request):
    if request.method == "POST":
        cycle_name = request.POST.get("CycleName")
        project = request.POST.get("Project")
        cycle_level = request.POST.get("CycleLevel")
        page = request.POST.get("page")
        if cycle_name:
            try:
                TestCycle.objects.create(CycleName=cycle_name,Project=project,CycleLevel=cycle_level)
                result = {"code": 0, "message": "TestCycle创建成功!"}
            except Exception as e:
                result = {"code": 1, "message": str(e)}
        else:
            result = {"code": 1, "message": "必须指定名称!"}
        return HttpResponseRedirect('/cccs/test_cycles?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page))

def update_test_cycle(request):
    '''
    更新TestCycle
    :param request:
    :return:
    '''
    if request.method == "GET":
        tid = request.GET.get('tid',None)
        tc_obj = TestCycle.objects.filter(id=tid)
        tc_dict = tc_obj.values('id','CycleName','Project','CycleLevel','Status').first()
        # print(tc_dict)
        return HttpResponse(json.dumps(dict(tc_dict)))

    elif request.method == "POST":
        tid = request.POST.get("id")
        cycle_name = request.POST.get("CycleName",None)
        project = request.POST.get("Project",None)
        cycle_level = request.POST.get("CycleLevel",None)
        status = request.POST.get("Status",None)
        status = "ACTIVE" if status == 'on' else "INACTIVE"

        page = request.POST.get("page")

        form_data = {
            'CycleName':cycle_name,
            'Project':project,
            'CycleLevel':cycle_level,
            'Status':status,
        }

        tc_obj = TestCycle.objects.get(id=tid)
        try:
            for k ,v in form_data.items():
                setattr(tc_obj,k,v)
                tc_obj.save()
            result = {"code": 0, "message": "TestCycle更新成功！"}
        except Exception as e:
            print(e)
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/cccs/test_cycles?status={0}&message={1}&page={2}'.
                            format(result.get("code", ""),
                                   result.get("message", ""),
                                   page))


def test_plans(request,tc_id=""):
    '''
    test_plan列表
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
        tc_id = tc_id
        tc_obj = TestCycle.objects.get(id=tc_id)
        queryset = TestPlan.objects.filter(Q(Q(CaseName__contains=search_q) |
                                           Q(Status__contains=search_q))
                                          ,CycleID=tc_obj).distinct().order_by('-id')
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'cccs/test_plans.html',locals())

def add_test_plan(request):
    if request.method == "POST":
        case_name = request.POST.get("CaseName")
        loop_cnt = request.POST.get("LoopCnt")
        tc_id = request.POST.get("tc_id")
        page = request.POST.get("page")
        if case_name:
            try:
                TestPlan.objects.create(CaseName=case_name,LoopCnt=loop_cnt,CycleID_id=tc_id)
                result = {"code": 0, "message": "TestPlan创建成功!"}
            except Exception as e:
                result = {"code": 1, "message": str(e)}
        else:
            result = {"code": 1, "message": "必须指定名称!"}
        return HttpResponseRedirect('/cccs/test_plans/{3}/?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,tc_id))

def update_test_plan(request):
    '''
    更新TestCycle
    :param request:
    :return:
    '''
    if request.method == "GET":
        tid = request.GET.get('tid',None)
        tp_obj = TestPlan.objects.filter(id=tid)
        tp_dict = tp_obj.values('id','CaseName','LoopCnt','Status').first()
        # print(tp_dict)
        return HttpResponse(json.dumps(dict(tp_dict)))

    elif request.method == "POST":
        tc_id = request.POST.get("tc_id")
        tid = request.POST.get("id")
        case_name = request.POST.get("CaseName",None)
        loop_cnt = request.POST.get("LoopCnt",None)
        status = request.POST.get("Status",None)
        status = "ACTIVE" if status == 'on' else "INACTIVE"

        page = request.POST.get("page")

        form_data = {
            'CaseName':case_name,
            'LoopCnt':loop_cnt,
            'Status':status,
        }

        tp_obj = TestPlan.objects.get(id=tid)
        try:
            for k ,v in form_data.items():
                setattr(tp_obj,k,v)
                tp_obj.save()
            result = {"code": 0, "message": "TestPlan更新成功！"}
        except Exception as e:
            print(traceback.format_exc())
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/cccs/test_plans/{3}/?status={0}&message={1}&page={2}'.
                            format(result.get("code", ""),
                                   result.get("message", ""),
                                   page,tc_id))


def run_records(request,tc_id='',t_status=''):
    '''
    run_records列表
    :param request:
    :return:
    '''
    if request.method == "GET":
        # 通知栏
        task_status = request.GET.get("task_status", "")
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code":int(status),"message":message}
        tc_id = tc_id
        t_status = t_status
        search_q = request.GET.get("q","").strip()
        page = request.GET.get('page')
        q_query = Q(Q(TestRunName__contains=search_q)|
                    Q(Status__contains=search_q)|
                    Q(JIRAID__contains=search_q)|
                    Q(FWPkgName__contains=search_q)|
                    Q(SrtPkgName__contains=search_q)
                    # Q(secsession_obj__father_session__title__contains=search_q)
                    )

        tc_obj = TestCycle.objects.get(id=tc_id)
        if t_status == "NOTSTART":
            queryset = TestRun.objects.filter(q_query,Status="NOTSTART",TCID=tc_obj).order_by('-id')
        elif t_status == "FINISHED":
            queryset = TestRun.objects.filter(q_query,Status="FINISHED",TCID=tc_obj).order_by('-id')
        elif t_status == "FAILED":
            queryset = TestRun.objects.filter(q_query,Status="FAILED",TCID=tc_obj).order_by('-id')
        elif t_status == "CANCELED":
            queryset = TestRun.objects.filter(q_query,Status="CANCELED",TCID=tc_obj).order_by('-id')
        elif t_status == "RUNNING":
            queryset = TestRun.objects.filter(q_query,Status="RUNNING",TCID=tc_obj).order_by('-id')
        else:
            queryset = TestRun.objects.filter(q_query, TCID=tc_obj).order_by('-id')
        # 加载分页器
        queryset, page_html = init_paginaion(request, queryset)

        return render(request,'cccs/run_records.html',locals())

def add_test_run(request):
    if request.method == "POST":
        tc_id = request.POST.get("tc_id")
        test_run_name = request.POST.get("TestRunName")
        trigger_time = request.POST.get("TriggerTime")
        jira_id = request.POST.get("JIRAID")
        page = request.POST.get("page")
        if test_run_name:
            try:
                TestRun.objects.create(TestRunName=test_run_name,TriggerTime=trigger_time,
                                       JIRAID=jira_id,TCID_id=tc_id )
                result = {"code": 0, "message": "TestRun创建成功!"}
            except Exception as e:
                result = {"code": 1, "message": str(e)}
        else:
            result = {"code": 1, "message": "必须指定名称!"}
        return HttpResponseRedirect('/cccs/run_records/{3}//?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,tc_id))

def update_test_run(request):
    '''
    更新TestCycle
    :param request:
    :return:
    '''
    if request.method == "GET":
        tid = request.GET.get('tid',None)
        tr_obj = TestRun.objects.filter(id=tid)
        tr_dict = dict(tr_obj.values('id','TestRunName','JIRAID','Comments').first())
        # trigger_time = tr_obj.first().TriggerTime
        # if trigger_time:
        #     tr_dict['TriggerTime'] = trigger_time.strftime("%Y-%m-%d  %H:%m:%s")
        # print(tr_dict)
        return HttpResponse(json.dumps(tr_dict))

    elif request.method == "POST":
        tc_id = request.POST.get("tc_id")
        tid = request.POST.get("id")
        tr_name = request.POST.get("TestRunName",None)
        jira_id = request.POST.get("JIRAID",None)
        comments = request.POST.get("Comments",None)
        # trigger_time = request.POST.get("TriggerTime",None)
        page = request.POST.get("page")

        form_data = {
            'TestRunName':tr_name,
            'JIRAID':jira_id,
            'Comments':comments,
            # 'TriggerTime':trigger_time,
        }

        tc_obj = TestRun.objects.get(id=tid)
        try:
            for k ,v in form_data.items():
                setattr(tc_obj,k,v)
                tc_obj.save()
            result = {"code": 0, "message": "TestRun更新成功！"}
        except Exception as e:
            print(traceback.format_exc())
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/cccs/run_records/{3}//?status={0}&message={1}&page={2}'.
                            format(result.get("code", ""),
                                   result.get("message", ""),
                                   page,tc_id))

def del_test_run(request):
    if request.method == "GET":
        tr_id = request.GET.get("tr_id")
        tc_id = request.GET.get("tc_id")
        page = request.GET.get("page")
        try:
            TestRun.objects.get(id=tr_id).delete()
            result = {"code": 0, "message": "TestRun删除成功!"}
        except Exception as e:
            result = {"code": 1, "message": str(e)}

        return HttpResponseRedirect('/cccs/run_records/{3}//?status={0}&message={1}&page={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           page,tc_id))

def actions(request,tc_id="",tp_id=""):
    '''
    状态变更记录
    :param request:
    :return:
    '''
    if request.method == "GET":
        # 通知栏
        task_status = request.GET.get("task_status", "")
        status = request.GET.get("status", "")
        message = request.GET.get("message", "")
        if status.isdigit():
            result = {"code": int(status), "message": message}

        tc_id = tc_id
        tp_id = tp_id

        search_q = request.GET.get("q","").strip()
        stime = request.GET.get("start_time","2019-01-01")
        etime = request.GET.get("end_time",datetime.datetime.now().strftime('%Y-%m-%d'))
        page = request.GET.get('page')

        q_query = Q(Q(OriginalVal__contains=search_q)|
                    Q(NewVal__contains=search_q)|
                    Q(ActionOP__contains=search_q)
                    )

        if tc_id: #从test_cycles访问
            tc_obj = TestCycle.objects.get(id=tc_id)
            queryset = TestAction.objects.filter(q_query,CycleID_id=tc_id,ActionTime__range=(stime,etime)).order_by("-id")
        elif tp_id: #从test_plans访问
            tp_obj = TestPlan.objects.get(id=tp_id)
            queryset = TestAction.objects.filter(q_query,PlanID_id=tp_id,ActionTime__range=(stime,etime)).order_by("-id")
        else:
            queryset = TestAction.objects.filter(q_query,ActionTime__range=(stime,etime)).order_by("-id")
        # 加载分页器
        queryset, page_html = init_paginaion(request, queryset)

        return render(request, 'cccs/test_actions.html', locals())