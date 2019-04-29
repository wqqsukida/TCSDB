from django.shortcuts import render,HttpResponse
from utils.auth_token import api_auth
from django.utils.decorators import method_decorator
from django.views import View
import json


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