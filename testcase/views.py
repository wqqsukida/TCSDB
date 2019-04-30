from django.shortcuts import render,HttpResponse
from utils.auth_token import api_auth
from django.utils.decorators import method_decorator
from django.views import View
import json
import copy
from utils.pagination import Pagination

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

class ApiList(View):
    @method_decorator(api_auth)
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'only post method!'}
        return HttpResponse(response)

    @method_decorator(api_auth)
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