# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 4/29/19 1:45 PM
# FileName: create_admin.py
import os
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TCSDB.settings')

import django
django.setup()

from django.db import transaction
from utils import md5
from rbac.models import  *
import getpass


username = input('Username:')
password = getpass.getpass('Password:')
re_password = getpass.getpass('Password(again):')

if password != re_password:
    print("Error: Your passwords didn't match.")
    exit(1)
else:
    try:
        with transaction.atomic():
            password = md5.encrypt(password)
            user_obj = UserProfile.objects.create(name=username,is_admin=True)
            AdminInfo.objects.create(username=username, password=password,
                                     user=user_obj)
        result = {"code": 0, "message": "创建用户成功！"}
        print('Create user succeed')
    except Exception as e:
        result = {"code": 1, "message": e}
        print(e)