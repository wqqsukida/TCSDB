# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 7/3/19 5:41 PM
# FileName: api.py
from utils.auth_token import APIAuthView,APITokenAuthView
from django.shortcuts import HttpResponse
from django.db import transaction
import json,traceback
import datetime
from result.models import *
from django.db.models import Max
from django.conf import settings

TEST = settings.TESTING