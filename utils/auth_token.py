# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 4/29/19 3:30 PM
# FileName: auth_token.py
from django.shortcuts import HttpResponse
from utils.md5 import encrypt
from django.conf import settings
import json

key = settings.API_TOKEN

def api_auth(func):
    def inner(request,*args,**kwargs):
        auth_header_val = request.META.get('HTTP_AUTH_TOKEN')
        # print('====================Auth-Token=====================')
        # print(auth_header_val)
        # print('===================================================')
        # 841770f74ef3b7867d90be37c5b4adfc|1506571253.9937866
        if auth_header_val:
            client_md5_str, client_ctime = auth_header_val.split('|', maxsplit=1)

            server_md5_str = encrypt("%s|%s" % (key, client_ctime,))
            if server_md5_str != client_md5_str:
                res = {'code': 6, 'msg': 'Token validtation failed!'}
                return HttpResponse(json.dumps(res))

            return func(request,*args,**kwargs)
        else:
            res = {'code': 7, 'msg': 'Can not found token,request failed!'}
            return HttpResponse(json.dumps(res))

    return inner