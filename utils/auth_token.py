# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 4/29/19 3:30 PM
# FileName: auth_token.py
from django.shortcuts import HttpResponse
from utils.md5 import encrypt
from django.conf import settings
import json
from rest_framework.views import APIView
from rbac.models import AdminInfo

key = settings.API_TOKEN

class LoginAuth(APIView):
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'Request method error!'}
        return HttpResponse(json.dumps(response))

    def post(self,request,*args,**kwargs):
        user = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        response = {'code': 4, 'msg': 'username or password is not correct!', 'data': None}
        if user and pwd:
            pwd = encrypt(pwd)  # md5加密密码字符串
            user_obj = AdminInfo.objects.filter(username=user, password=pwd).first()
            if user_obj:
                request.session['api_auth'] = {'user': user_obj.user.name}

                response = {'code':3,'msg':'Login successfully!'}
        print(response)


        return HttpResponse(json.dumps(response))

class APIAuthView(APIView):
    def dispatch(self, request, *args, **kwargs):
        login = request.session.get('api_auth')
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            clien_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            clien_ip = request.META['REMOTE_ADDR']
        if settings.TESTING:
            return super().dispatch(request, *args, **kwargs)
        if not login:
            res = {'code': 7, 'msg': 'API validtation failed!'}
            print('[{0}]:{1}'.format(clien_ip, res))
            return HttpResponse(json.dumps(res))
        if not request.body:
            res = {'code': 6, 'msg': 'The request body can not be null!'}
            print('[{0}]:{1}'.format(clien_ip, res))
            return HttpResponse(json.dumps(res))

        return super().dispatch(request, *args, **kwargs)

class APITokenAuthView(APIView):
    def dispatch(self, request, *args, **kwargs):
        # server_float_ctime = time.time()
        auth_header_val = request.META.get('HTTP_AUTH_TOKEN')
        # 841770f74ef3b7867d90be37c5b4adfc|1506571253.9937866
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            clien_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            clien_ip = request.META['REMOTE_ADDR']

        if auth_header_val:
            client_md5_str, client_ctime = auth_header_val.split('|', maxsplit=1)
            # client_float_ctime = float(client_ctime)
            # print(server_float_ctime - client_float_ctime)
            # if (client_float_ctime + 20) < server_float_ctime :
            #     res = {'code': 5, 'msg': 'token已经过期!'}
            #     print('[{0}]:{1}'.format(clien_ip, res))
            #     return HttpResponse(json.dumps(res))

            # if client_md5_str in SIGN_RECORD:
            #     res = {'code': 6, 'msg': 'token已被使用!'}
            #     print('[{0}]:{1}'.format(clien_ip, res))
            #     return HttpResponse(json.dumps(res))

            server_md5_str = encrypt("%s|%s" % (key, client_ctime,))
            if server_md5_str != client_md5_str:
                res = {'code': 7, 'msg': 'Token validtation failed!'}
                print('[{0}]:{1}'.format(clien_ip, res))
                return HttpResponse(json.dumps(res))

            # SIGN_RECORD[server_md5_str] = client_ctime
            # SIGN_RECORD_copy = copy.deepcopy(SIGN_RECORD)
            # for k,v in SIGN_RECORD_copy.items():
            #     if float(v) + 20 < float(client_ctime):
            #         SIGN_RECORD.pop(k)

            # print(SIGN_RECORD)
        else:
            res = {'code': 8, 'msg': 'Can not found token,request failed!'}
            print('[{0}]:{1}'.format(clien_ip, res))
            return HttpResponse(json.dumps(res))

        return super().dispatch(request, *args, **kwargs)