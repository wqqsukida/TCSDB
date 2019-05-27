# /usr/bin/env python
# -*- coding:utf-8 -*-
# Author  : wuyifei
# Data    : 5/13/19 3:03 PM
# FileName: api.py
from django.shortcuts import render,HttpResponse
from utils.auth_token import APIAuthView
import json
from django.db import transaction
from testcase.models import *
from copy import deepcopy
from django.db.models import Q
import traceback

class AddDataBase(APIAuthView):
    """
    """
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'Request method error!'}
        return HttpResponse(json.dumps(response))

    def post(self,request,*args,**kwargs):
        print(request.POST)
        res = request.data.get("data")
        print(res)
        response = self.addData(res)
        return HttpResponse(json.dumps(response, indent=4))
    
    def addData(self, res):
        """
        """
        pass

class AddRefSpec(AddDataBase):
    '''
            新增参考文档信息
    '''
    def addData(self, res):
        """
        """
        try:
            refer_obj = ReferSpec.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':refer_obj.id}
        except Exception as e:
            response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return response

class AddTestPoint(AddDataBase):
    '''
            新增测试点信息
    '''
    def addData(self, res):
        """
        """
        spec_point = res.pop("SpecAndPoint")
        spec_list = spec_point.split(",")
        try:
            tp_obj = TestPoint.objects.create(**res)
            tp_obj.save()
            tp_obj.SpecAndPoint.set(spec_list)
            response = {'code':0,'msg':'Success!','data':tp_obj.id}
        except Exception as e:
            response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return response

class AddCaseDesc(AddDataBase):
    '''
            新增测试用例信息
    '''
    def addData(self, res):
        """
        """
        case_point = res.pop("CaseAndPoint")
        point_list = case_point.split(",")
        try:
            ts_obj = TestCaseDetail.objects.create(**res)
            ts_obj.save()
            if len(point_list) > 0:
                ts_obj.CaseAndPoint.set(point_list)
            response = {'code':0,'msg':'Success!','data':ts_obj.id}
        except Exception as e:
            response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':{}}
        return response

class UpdateCaseBase(APIAuthView):
    '''
            更新测试测试用例相关选项
    '''
    def post(self,request,*args,**kwargs):
        res = request.data.get("data")
        response = self.updateData(res)
        return HttpResponse(json.dumps(response,indent=4))
    
    def updateData(self, res):
        """
        """
        try:
            with transaction.atomic():
                case_name = res.pop('CaseName')
                case_obj = TestCaseDetail.objects.filter(CaseName=case_name)
                if len(case_obj) == 0:
                    response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(case_name),'data':False}
                else:
                    case_obj.update(**res)
                    response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':False}
        return response

class UpdateCaseStep(UpdateCaseBase):
    '''
            更新测试用例步骤信息
    '''
    def updateData(self, res):
        try:
            with transaction.atomic():
                case_name = res.pop('CaseName')
                case_obj = TestCaseDetail.objects.filter(CaseName=case_name).first()
                case_step_obj = case_obj.case_step.filter(Step=res["Step"])
                if len(case_step_obj) == 0:
                    response = {'code':6,'msg':'Step:{0} not exist, please check!!'.format(res["Step"]),'data':False}
                else:
                    case_step_obj.update(**res)
                    response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':False}
        return response

class UpdateCaseProject(UpdateCaseBase):
    '''
            新增/更新测试用例项目信息
    '''   
    def updateData(self, res):
        """
        """
        try:
            with transaction.atomic():
                case_name = res.pop('CaseName')
                pj_name = res["Project"]
                case_status = res["Status"].upper()
                res["Status"] = case_status
                case_obj = TestCaseDetail.objects.filter(CaseName=case_name).first()
                project_obj = case_obj.case_project.filter(Project=pj_name)
                print("select case is:%s" % case_obj)
                print("project_obj :%s" % project_obj)
                
                if len(project_obj) == 0:#add new item in project
                    try:
                        with transaction.atomic():
                            pj_obj = TestProject(Project=pj_name, Status=case_status.upper())
                            pj_obj.save()
                            pj_obj.TID.add(case_obj)
                            response = {'code':0,'msg':'Success!','data':True}
                    except Exception as e:
                        response = {'code':7,'msg':'Case:{0} add project{1} fail, err:{2}'.format(case_name, pj_name, str(e)),'data':False}
                else:#update existed item
                    #check modify content
                    pj_ins = project_obj.first()
                    if pj_ins.Project == pj_name and pj_ins.Status == case_status:
                        response = {'code':8,'msg':'Case:{0} modify project:{1} fail, same with current value'.format(case_name, pj_name),'data':False}
                    else:
                        project_obj.update(**res)
                        response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':False}
        return response

class UpdateCaseVersion(UpdateCaseBase):
    '''
            更新测试用例版本信息
    '''
    pass

class UpdateCaseSrtInfo(UpdateCaseBase):
    '''
            更新测试用例脚本相关信息
    '''
    pass

class UpdateCaseOwnership(UpdateCaseBase):
    '''
            更新测试用例脚本所有者相关信息
    '''
    pass

class UpdateCaseCategory(UpdateCaseBase):
    '''
            更新测试用例脚本属类相关信息
    '''
    pass

class UpdateCaseLabels(UpdateCaseBase):
    '''
            更新测试用例脚本标签相关信息
    '''
    pass

class UpdateCaseDepInfo(UpdateCaseBase):
    '''
            更新测试用例脚本其他相关信息
    '''
    pass

class GetCaseInfoBase(APIAuthView):
    """
            获取用例的一些相关信息
    """
    def getItemList(self):
        """
        """
        pass

    def get(self,request,*args,**kwargs):
        res = request.data.get("data")
        response = self.getData(res)
        return HttpResponse(json.dumps(response,indent=4))
    
    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        data_dic = {}
        try:
            case_name = res.get('CaseName')
            case_obj = TestCaseDetail.objects.filter(CaseName=case_name)
            case_ins = case_obj.first()
            if len(case_obj) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(case_name),'data':""}
            else: 
                for item in get_list:
                    data_dic[item] = getattr(case_ins, item)
                response = {'code': 0, 'msg': 'Success!', 'data': data_dic}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class GetCaseScriptInfo(GetCaseInfoBase):
    '''
            获得用例的脚本的基本信息
    '''
    def getItemList(self):
        return ("CaseName", "ScriptName", "ScriptPath", "ScriptParams")

class GetCaseSrtOwner(GetCaseInfoBase):
    '''
            获得用例的负责者的基本信息
    '''
    def getItemList(self):
        return ("Owner", "BackupOwner")


class GetCaseDetailedInfo(GetCaseInfoBase):
    """
            获得用例的详细信息
    """
    def getItemList(self):
        return ("id", "CaseName", "Description", "ScriptName", "ScriptPath", "ScriptParams", "Version",
               "Author",  "Owner", "BackupOwner", "Automated", "Importance", "Level", "Category", "Subcategory",
               "Labels", "HWRequired", "SWRequired", "VSRequired", "DrvSupported", "OSSupported", "OEMSupported",
               "SKUSupported")

class GetCaseStepInfo(GetCaseInfoBase):
    """
            获得用例的测试步骤信息
    """
    def getItemList(self):
        return("id", "Step", "StepType", "StepDesc", "ExpectRslt")

    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        try:
            case_name = res.get('CaseName')
            case_all = TestCaseDetail.objects.filter(CaseName=case_name)
            case_obj = case_all.first()
            case_steps = case_obj.case_step.all()
            if len(case_all) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(case_name),'data':""}
            else: 
                case_step_list = []
                for s in case_steps:
                    data_dic = {}
                    for item in get_list:
                        data_dic[item] = getattr(s, item)
                    case_step_list.append(data_dic)
                response = {'code': 0, 'msg': 'Success!', 'data': case_step_list}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response
    
class GetCaseTestPoints(GetCaseInfoBase):
    """
            获得用例的详细测试点信息
    """
    def getData(self, res):
        """
        """
        pt_List = ["id", "TestDesc", "SelectFrom", "PageNo"]
        sp_List = ["FileName", "Version"]
        try:
            case_name = res.get('CaseName')
            case_all = TestCaseDetail.objects.filter(CaseName=case_name)
            case_obj = case_all.first()
            case_points = case_obj.CaseAndPoint.all().distinct()
            print("case_points :%s" % case_points)
            if len(case_all) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(case_name),'data':""}
            else:
                case_point_list = []
                for p in case_points:
                    data_dic = {}
                    tp_dic = {}
                    for item in pt_List:
                        tp_dic[item] = getattr(p, item)
                    point_specs = p.SpecAndPoint.all()
                    print("point_specs :%s" % point_specs)
                    for s in point_specs:
                        data_dic = deepcopy(tp_dic)
                        for item in sp_List:
                            data_dic[item] = getattr(s, item)
                        case_point_list.append(data_dic)
                response = {'code': 0, 'msg': 'Success!', 'data': case_point_list}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class GetCaseProjectInfo(GetCaseInfoBase):
    """
            获得用例项目状态信息
    """
    def getItemList(self):
        return("Project", "Status")

    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        try:
            case_name = res.get('CaseName')
            case_all = TestCaseDetail.objects.filter(CaseName=case_name)
            case_obj = case_all.first()
            case_pjs = case_obj.case_project.all()
            if len(case_all) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(case_name),'data':""}
            else: 
                case_project_list = []
                for pj in case_pjs:
                    data_dic = {}
                    for item in get_list:
                        data_dic[item] = getattr(pj, item)
                    case_project_list.append(data_dic)
                response = {'code': 0, 'msg': 'Success!', 'data': case_project_list}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class GetProjectCases(GetCaseInfoBase):
    """
            获得项目测试用例列表
    """
    def getItemList(self):
        return("id", "CaseName")

    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        filter_dic = {}
        depend_search = False
        pj           = res.get("Project")
        case_status  = res.get("Status")
        case_level   = res.get("Level")
        case_label   = res.get("Labels")
        case_impt    = res.get("Importance")
        case_auto    = res.get("Automated")
        case_depends = res.get("Depends")
        print("pj:%s,case_status:%s,case_level:%s,case_label:%s,case_impt:%s,case_auto:%s, case_depends:%s" 
              % (pj, case_status,case_level, case_label, case_impt, case_auto, case_depends))
        if pj is not None:
            filter_dic["Project"] = pj
        if case_status is not None:
            filter_dic["Status"] = case_status
        if case_level is not None and case_level != "All":
            filter_dic["TID__Level__icontains"] = case_level
        if case_label is not None:
            filter_dic["TID__Labels__icontains"] = case_label
        if case_impt is not None:
            filter_dic["TID__Importance__lte"] = case_impt
        filter_dic["TID__Automated"] = "True" if case_auto is None else case_auto
        if case_depends is not None:
            depend_search = True
        try:
            print("filter_dic is:%s" % filter_dic)
            if depend_search == False:
                prj_obj = TestProject.objects.filter(**filter_dic).distinct()
            else:
                prj_obj = TestProject.objects.filter((Q(TID__HWRequired__icontains=case_depends)|Q(TID__SWRequired__icontains=case_depends)\
                                                      |Q(TID__VSRequired__icontains=case_depends)|Q(TID__DrvSupported__icontains=case_depends)\
                                                      |Q(TID__OSSupported__icontains=case_depends)|Q(TID__OEMSupported__icontains=case_depends)\
                                                      |Q(TID__SKUSupported__icontains=case_depends)), **filter_dic).distinct()
            print(prj_obj)
            if len(prj_obj) == 0:
                response = {'code':6,'msg':'Case list is null, please check!!','data':""}
            else:
                case_list = []
                for c in prj_obj:
                    case_obj = c.TID.all().first()
                    data_dic = {}
                    for item in get_list:
                        data_dic[item] = getattr(case_obj, item)
                        data_dic["Project"] = c.Project
                    case_list.append(data_dic)
                response = {'code': 0, 'msg': 'Success!', 'data': case_list}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}

        return response

class AddPerfTestItem(APIAuthView):
    '''
    新增性能测试项
    '''
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'Request method error!'}
        return HttpResponse(json.dumps(response))

    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}

        return HttpResponse(json.dumps(response))

class AddToolTestItem(APIAuthView):
    '''
    新增兼容性测试项
    '''
    def get(self,request,*args,**kwargs):
        response = {'code':1,'msg':'Request method error!'}
        return HttpResponse(json.dumps(response))

    def post(self,request,*args,**kwargs):
        print(request.POST)
        '''
        query...
        '''
        response = {'code':0,'msg':'Success!','data':{}}

        return HttpResponse(json.dumps(response))
