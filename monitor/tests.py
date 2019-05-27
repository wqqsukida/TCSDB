from django.test import TestCase
from django.test import Client
from rest_framework.test import APIRequestFactory
import requests, json
import time
import hashlib
from requests.cookies import RequestsCookieJar
from django.conf import settings
from monitor.api import *
# Create your tests here.
# server_ip = '10.0.2.20:8080'
#
# import inspect
#
#
# def get_current_function_name():
#     return inspect.stack()[1][3]


# class ApiTest(TestCase):
#     @property
#     def cookies(self):
#         rep = requests.post('http://{0}/api/auth/'.format(server_ip), data={'username': 'admin', 'password': 'admin'})
#         cookie_jar = RequestsCookieJar()
#         cookie_jar.set(name='sessionid', value=rep.cookies['sessionid'])
#         return cookie_jar
#
#     def add_dut(self):
#         rep = requests.post('http://{0}/monitor/api/dut/add/'.format(server_ip),cookies=self.cookies,
#                            json={"data":{"SerialNum":"sn10","DeviceType":5,"Manufactured":"2019-05-16 16:50:37"}})
#         data = json.loads(rep.text)
#         if data.get("data"):
#             print("[%s]:Run Successfully!"%get_current_function_name())
#         else:
#             print("[%s]:[%s]"%(get_current_function_name(),data))
#
#     def dut_get_info(self):
#         rep = requests.get('http://{0}/monitor/api/dut/get_info/'.format(server_ip),cookies=self.cookies,
#                            json={"data":{"SerialNum":"sn01"}})
#         data = json.loads(rep.text)
#         if data.get("data"):
#             print("[%s]:Run Successfully!"%get_current_function_name())
#         else:
#             print("[%s]:[%s]"%(get_current_function_name(),data))
#
# a = ApiTest()
# a.add_dut()
# a.dut_get_info()


class ApiTest(TestCase):

    @property
    def auth_header_val(self):
        ctime = str(time.time())
        new_key = "%s|%s" % (settings.API_TOKEN, ctime,)  # asdfuasodijfoausfnasdf|时间戳
        hs = hashlib.md5()
        hs.update(new_key.encode('utf-8'))
        md5_str = hs.hexdigest()
        auth_header_val = "%s|%s" % (md5_str, ctime,)  # 6f800b6a11d3f9c08c77ef8f77b2d460|时间戳
        return auth_header_val


    def add_dut(self):
        c = Client(HTTP_AUTH_TOKEN=self.auth_header_val)
        # # rep = requests.post('127.0.0.1',headers={'auth-token':self.auth_header_val})
        rep = c.post('/monitor/api/dut/add/',content_type='application/json',
                     data={
                         "data":{
                             "SerialNum": "sn12",
                             "DeviceType": 5,
                             "Manufactured": "2019-05-16 16:50:37"
                         }})
        # self.assertEqual(rep.get("code"),0)
        print(rep.status_code)
        print(rep.content)

# a = ApiTest()
# a.add_dut()
