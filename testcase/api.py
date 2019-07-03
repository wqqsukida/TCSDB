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
    新增项目的基类
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
    """
            新增测试点信息
    """
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
        #print(res)
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
            新增/更新测试用例步骤信息
    '''
    def updateData(self, res):
        try:
            with transaction.atomic():
                case_name = res.pop('CaseName')
                case_obj = TestCaseDetail.objects.filter(CaseName=case_name).first()
                case_step_obj = case_obj.case_step.filter(Step=res["Step"])
                if len(case_step_obj) == 0:#add a new test case step
                    try:
                        with transaction.atomic():
                            step_obj = CaseStep(Step=res["Step"], StepType=res["StepType"], StepDesc=res["StepDesc"],
                                                ExpectRslt=res["ExpectRslt"], TID=case_obj)
                            step_obj.save()
                            response = {'code':0,'msg':'Success!','data':True}
                    except Exception as e:
                        response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':False}
                else:
                    print("update")
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
        response = {'code':1,'msg':'Request method error!'}
        return HttpResponse(json.dumps(response))

    def post(self,request,*args,**kwargs):
        print(request.POST)
        res = request.data.get("data")
        print(res)
        response = self.getData(res)
        return HttpResponse(json.dumps(response, indent=4))

#     def get(self,request,*args,**kwargs):
#         res = request.data.get("data")
#         print("res is:%s" % res)
#         response = self.getData(res)
#         return HttpResponse(json.dumps(response,indent=4))
    
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

class AddPerfTestItem(AddDataBase):
    '''
            新增性能测试项目
    '''
    def addData(self, res):
        """
        """
        try:
            perf_obj = PerfTestItem.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':False}
        return response

class AddPerfGlobal(AddDataBase):
    '''
            新增性能全局
    '''
    def addData(self, res):
        """
        """
        try:
            perf_obj = PerfGlobal.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':False}
        return response

class AddPerfTestCase(AddDataBase):
    '''
            新增性能测试用例
    '''
    def addData(self, res):
        """
        """
        global_name = res.pop("GlobalName")
        global_obj = PerfGlobal.objects.filter(GlobalName=global_name)
        if len(global_obj) == 0:
            response = {'code':6,'msg':'global case name:' + global_name+"doesn't exist, please check!!",'data':""}
        else:
            res["TIID"] = global_obj.first()
            try:
                perf_obj = PerfTestCase.objects.create(**res)
                response = {'code':0,'msg':'Success!','data':True}
            except Exception as e:
                response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':False}
        return response

class AddItemIntoCase(AddDataBase):
    '''
            新增性能测试项目和测试用例对应关系
    '''
    def addData(self, res):
        """
        """
        case_name = res.pop("CaseName")
        item_name = res.pop("ItemName")
        case_obj = PerfTestCase.objects.filter(CaseName=case_name)
        item_obj = PerfTestItem.objects.filter(ItemName=item_name)
        if len(case_name) == 0:
            response = {'code':6,'msg':'case name:' + case_name +"doesn't exist, please check!!",'data':""}
        else:
            if len(item_obj) == 0:
                response = {'code':6,'msg':'item name:' + item_name +"doesn't exist, please check!!",'data':""}
            else:
                res["TIID"] = item_obj.first()
                res["TCID"] = case_obj.first()
                try:
                    perf_obj = PerfItemInCase.objects.create(**res)
                    response = {'code':0,'msg':'Success!','data':True}
                except Exception as e:
                    response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':False}
        return response

class AddItemRefVal(AddDataBase):
    '''
            新增项目参考值
    '''
    def addData(self, res):
        """
        """
        case_name = res.pop("CaseName")
        item_name = res.pop("ItemName")
        print("*** case name:%s, item name:%s" %(case_name, item_name))
        case_item_obj = PerfItemInCase.objects.filter(TCID__CaseName=case_name, TIID__ItemName=item_name)
        if len(case_item_obj) == 0:
            response = {'code':6,'msg':'case name:' + case_name +'item name:'+item_name+" doesn't exist, please check!!",'data':""}
        else:
            res["IICID"] = case_item_obj.first()
            print("*** iicid:%s" % res["IICID"])
            try:
                perf_obj = PerfRefTarget.objects.create(**res)
                response = {'code':0,'msg':'Success!','data':True}
            except Exception as e:
                response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':False}
        return response

class GetCaseTestItems(GetCaseInfoBase):
    """
            获得用例测试项目
    """
    def getItemList(self):
        return("ItemName")

    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        case_name = res.get('CaseName')
        case_obj = PerfTestCase.objects.filter(CaseName=case_name)
        if len(case_obj) == 0:
            response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(case_name),'data':""}
        else:
            try:
                item_list = PerfItemInCase.objects.filter(TCID=case_obj.first())
                case_item_list = []
                for item in item_list:
                    data_dic = {}
                    data_dic["ItemName"] = item.TIID.ItemName
                    case_item_list.append(data_dic)
                print(case_item_list)
                response = {'code': 0, 'msg': 'Success!', 'data': case_item_list}
            except Exception as e:
                print(traceback.format_exc())
                response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class GetPerfGlobal(GetCaseInfoBase):
    """
            获得用例全局信息
    """
    def getItemList(self):
        return("GlobalName", "MaxIOSize", "Offset", "NeedPurge", "Need2XFillDriver")

    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        global_name = res.get('GlobalName')
        try:
            case_obj = PerfGlobal.objects.filter(GlobalName=global_name)
            case_list = case_obj.first()
            if len(case_obj) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(global_name),'data':""}
            else:
                data_dic = {}
                for item in get_list:
                    data_dic[item] = getattr(case_list, item)
                response = {'code': 0, 'msg': 'Success!', 'data': data_dic}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class GetTestCase(GetCaseInfoBase):
    """
            获得Perf用例信息
    """
    def getItemList(self):
        return("CaseName", "CaseType")
    
    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        case_name = res.get('CaseName')
        try:
            case_obj = PerfTestCase.objects.filter(CaseName=case_name)
            case_item = case_obj.first()
            if len(case_obj) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(case_name),'data':""}
            else:
                data_dic = {}
                global_name= case_item.TIID.GlobalName
                data_dic["GlobalName"] = global_name
                for item in get_list:
                    data_dic[item] = getattr(case_item, item)
                response = {'code': 0, 'msg': 'Success!', 'data': data_dic}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class GetCaseItem(GetCaseInfoBase):
    """
            获得测试项信息
    """
    def getItemList(self):
        return("ItemName", "CheckPoint", "AccessPercent", "BlockSize", "BlockAlign", "IODepth", "RWMixRead",
               "RandPercent", "NumJobs", "RunTime", "StartDelay", "LoopCnt")
    
    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        item_name = res.get('ItemName')
        try:
            item_obj = PerfTestItem.objects.filter(ItemName=item_name)
            item_item = item_obj.first()
            if len(item_obj) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(item_name),'data':""}
            else:
                data_dic = {}
                for item in get_list:
                    data_dic[item] = getattr(item_item, item)
                response = {'code': 0, 'msg': 'Success!', 'data': data_dic}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class GetItemRefVal(GetCaseInfoBase):
    """
            获得测试项参考值
    """
    def getItemList(self):
        return("RefUnit", "RefVal")
    
    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        case_name = res.get("CaseName")
        item_name = res.get('ItemName')
        project_name = res.get('Project')
        filter_dic = {
                       "Project": project_name,
                       "IICID__TIID__ItemName__icontains":item_name,
                       "IICID__TCID__CaseName__icontains":case_name
                     }
        try:
            item_obj = PerfRefTarget.objects.filter(**filter_dic)
            item_item = item_obj.first()
            if len(item_obj) == 0:
                response = {'code':6,'msg':'Case:{0} item:{1} project:{2} not exist, please check!!'.format(case_name, item_name, project_name),'data':""}
            else:
                data_dic = {}
                for item in get_list:
                    data_dic[item] = getattr(item_item, item)
                response = {'code': 0, 'msg': 'Success!', 'data': data_dic}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class FindPerfTestCase(GetCaseInfoBase):
    """
            查找符合条件的测试用例
    """   
    def getData(self, res):
        """
        """
        filter_dic = {}
        test_level = res.get("Level")
        case_type = res.get('CaseType')
        if test_level is not None and test_level.upper() != "ALL":
            filter_dic["Level"]= test_level
        if case_type is not None and case_type.upper() != "ALL":
            filter_dic["CaseType"] = case_type
        try:
            item_obj = PerfTestCase.objects.filter(**filter_dic)
            if len(item_obj) == 0:
                response = {'code':6,'msg':'Case:{0} Level:{2} not exist, please check!!'.format(case_type, test_level),'data':""}
            else:
                case_list = []
                for item in item_obj:
                    data_dic = {}
                    data_dic["CaseName"] = item.CaseName
                    case_list.append(data_dic)
                response = {'code': 0, 'msg': 'Success!', 'data': case_list}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class AddToolTestItem(AddDataBase):
    '''
    新增兼容性测试项
    '''
    def addData(self, res):
        try:
            item_obj = CompTestItem.objects.create(**res)
            response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':False}
        return response

class AddToolTestCase(AddDataBase):
    '''
    新增兼容性用例项
    '''
    def addData(self, res):
        item_id = res.pop('TTID')
        item_obj = CompTestItem.objects.get(pk=item_id)
        res["TTID"] = item_obj
        if item_obj is None:
            response = {'code':6,'msg':'item:%s not exist' %item_id,'data':False}
        else:
            try:
                item_obj = CompTestCase.objects.create(**res)
                response = {'code':0,'msg':'Success!','data':True}
            except Exception as e:
                response = {'code':5, 'msg':'Service internal error:{0}'.format(str(e)),'data':False}
            return response

class UpdateToolProjectStatus(UpdateCaseBase):
    '''
    新增/更新兼容性测试项目的用例状态
    '''
    def updateData(self, res):
        try:
            with transaction.atomic():
                case_name = res.pop('CaseName')
                prj_name = res.pop('Project')
                status   = res.pop('Status')
                new_case_obj = CompTestCase.objects.filter(Name=case_name).first()
                case_obj = CompProject.objects.filter(Project=prj_name, TCID__Name__icontains=case_name)
                print("case_obj is:%s" % case_obj)
                if case_obj is None:#add a new test case into project
                    prj_obj = CompProject(Project=prj_name, Status=status)
                    prj_obj.save()
                    prj_obj.TCID.add(new_case_obj) 
                    response = {'code':6,'msg':'case:%s for project:%s not exist' %(case_name, prj_name),'data':False}
                else:
                    pj_ins = case_obj.first()
                    if pj_ins.Project == prj_name and pj_ins.Status == status:
                        response = {'code':8,'msg':'Case:{0} modify project:{1} fail, same with current value'.format(case_name, prj_name),'data':False}
                    else:
                        setattr(pj_ins, "Project", prj_name)
                        setattr(pj_ins, "Status", status)
                        pj_ins.TCID.set([new_case_obj])
                        pj_ins.save()
                        response = {'code':0,'msg':'Success!','data':True}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code':5,'msg':'Server internal error:{0}'.format(str(e)),'data':False}
        return response

class GetToolTestCase(GetCaseInfoBase):
    '''
获取兼容性测试用例的详情
    '''
    def getItemList(self):
        return("Name", "SupportOS", "OSVersion", "HWBrandReq", "HWModelReq", "HWReqLables", "DUTReqLables")
    
    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        item_name = res.get('Name')
        try:
            item_obj = CompTestCase.objects.filter(Name=item_name)
            item_item = item_obj.first()
            if len(item_obj) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(item_name),'data':""}
            else:
                data_dic = {}
                for item in get_list:
                    data_dic[item] = getattr(item_item, item)
                response = {'code': 0, 'msg': 'Success!', 'data': data_dic}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class GetToolTestItem(GetCaseInfoBase):
    '''
    获取兼容性测试项目的详情
    '''
    def getItemList(self):
        return("Name", "Description", "OSRequired", "Automated", "ToolName", "ToolVersion", "ToolPath",\
               "ToolParam", "Comments")
    
    def getData(self, res):
        """
        """
        get_list = self.getItemList()
        item_name = res.get('Name')
        try:
            item_obj = CompTestItem.objects.filter(Name=item_name)
            item_item = item_obj.first()
            if len(item_obj) == 0:
                response = {'code':6,'msg':'Case:{0} not exist, please check!!'.format(item_name),'data':""}
            else:
                data_dic = {}
                for item in get_list:
                    data_dic[item] = getattr(item_item, item)
                response = {'code': 0, 'msg': 'Success!', 'data': data_dic}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response

class FindCompProjTestCases(GetCaseInfoBase):
    '''
    获取满足搜索条件的测试用例信息
    '''
    def getData(self, res):
        """
        """
        filter_dic = {}
        prj_name = res.get("Project")
        case_status = res.get('Status')
        if prj_name is not None and prj_name.upper() != "ALL":
            filter_dic["Project"]= prj_name
        if case_status is not None and case_status.upper() != "ALL":
            filter_dic["Status"] = case_status
        try:
            item_obj = CompProject.objects.filter(**filter_dic)
            if len(item_obj) == 0:
                response = {'code':6,'msg':'Case:{0} project:{1} not exist, please check!!'.format(case_status, prj_name),'data':""}
            else:
                case_list = []
                for item in item_obj:
                    data_dic = {}
                    data_dic["Name"] = item.TCID.first().Name
                    case_list.append(data_dic)
                response = {'code': 0, 'msg': 'Success!', 'data': case_list}
        except Exception as e:
            print(traceback.format_exc())
            response = {'code': 5, 'msg': 'Server internal error:{0}'.format(str(e)), 'data': {}}
        return response
