# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 5/15/19 2:55 PM
# FileName: custom_execption.py
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        # print(response.data)
        response.data.clear()
        response.data['code'] = response.status_code
        response.data['data'] = None

        if response.status_code == 404:
            try:
                response.data['msg'] = response.data.pop('detail')
                response.data['msg'] = "Not found"
            except KeyError:
                response.data['msg'] = "Not found"

        if response.status_code == 400:
            response.data['msg'] = 'Input error'

        elif response.status_code == 401:
            response.data['msg'] = "Auth failed"

        elif response.status_code >= 500:
            response.data['msg'] =  "Internal service errors"

        elif response.status_code == 403:
            response.data['msg'] = "Access denied"

        elif response.status_code == 405:
            response.data['msg'] = 'Request method error !'
            response.data['code'] = 1
    return response