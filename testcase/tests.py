from django.test import TestCase, Client
from .models import *
from django.conf import settings
import json
 
# Create your tests here.
class TestCaseTests(TestCase):
    """
    Test RefSpec related API
    """
    def setUp(self):
        #create function test objects
        r1 = ReferSpec(FileName="UFS", Standard=True, Version="3.0", FilePath="C:\\Spec\\UFS")
        r1.save()
        r2 = ReferSpec(FileName="NVME", Standard=True, Version="3.0", FilePath="C:\\Spec\\Nvme")
        r2.save()
        tp1 = TestPoint(TestDesc="basicread", SelectFrom="fdafdafdaf", PageNo=10)
        tp1.save()
        tp1.SpecAndPoint.set([r1, r2])
        tp2 = TestPoint(TestDesc="basicwrite", SelectFrom="bbbbb", PageNo=10)
        tp2.save()
        tp3 = TestPoint(TestDesc="readoverlap", SelectFrom="ccccc", PageNo=20)
        tp3.save()
        tp2.SpecAndPoint.add(r2)
        ts1 = TestCaseDetail(CaseName="read1", Description="basic read", ScriptName="basicread.py",
                             ScriptPath="ibm-l2/dataTransfer", ScriptParams="--doPdb True", Version="1.0",
                             Author="cuimei", Owner="cuimei", BackupOwner="xuhui", Automated=True, Importance=20,
                             Level="L2", Category="BCI", Subcategory="M", Labels="test", HWRequired="hwread",
                             SWRequired="sw", VSRequired="Y", DrvSupported="drive", OSSupported="windows", 
                             OEMSupported="lenovo", SKUSupported="8160")
        ts1.save()
        ts1.CaseAndPoint.set([tp1, tp2])
        ts2 = TestCaseDetail(CaseName="write1", Description="basic write", ScriptName="basicwrite.py",
                             ScriptPath="ibm-l2/dataTransfer", ScriptParams="--doPdb True", Version="1.0",
                             Author="cuimei", Owner="cuimei", BackupOwner="xuhui", Automated=True, Importance=20,
                             Level="L2", Category="BCI", Subcategory="M", Labels="test", HWRequired="hw",
                             SWRequired="sw", VSRequired="Y", DrvSupported="drive", OSSupported="windows", 
                             OEMSupported="lenovo", SKUSupported="8160")
        ts2.save()
        ts2.CaseAndPoint.add(tp1)
        tprj1 = TestProject(Project="TaiPlus", Status="TODO")
        tprj1.save()
        tprj1.TID.add(ts1)
        tprj2 = TestProject(Project="TaiPlus", Status="TODO")
        tprj2.save()
        tprj2.TID.add(ts2)
        cs1 = CaseStep(Step=1, StepType="MAIN", StepDesc="write some data", ExpectRslt="pass", TID=ts1)
        cs1.save()
        cs2 = CaseStep(Step=2, StepType="MAIN", StepDesc="read and compare data", ExpectRslt="pass", TID=ts1)
        cs2.save()
        cs3 = CaseStep(Step=1, StepType="MAIN", StepDesc="write some data to drive", ExpectRslt="pass", TID=ts2)
        cs3.save()
        #create performance test objects
        perfg1 = PerfGlobal(GlobalName="fio", MaxIOSize=100, Offset=0, NeedPurge=True, Need2XFillDriver=False)
        perfg1.save()
        perfg2 = PerfGlobal(GlobalName="bonnie", MaxIOSize=0, Offset=50, NeedPurge=False, Need2XFillDriver=True)
        perfg2.save()
        
        perfitem1 = PerfTestItem(ItemName="test1", CheckPoint="FOB", AccessPercent=100, BlockSize=4096,
                                 BlockAlign=4096, IODepth=64, RWMixRead=30, RandPercent=0, NumJobs=2,
                                 RunTime=3600, StartDelay=0, LoopCnt=10)
        perfitem1.save()
        perfitem2 = PerfTestItem(ItemName="test2", CheckPoint="SSS", AccessPercent=100, BlockSize=4096,
                                 BlockAlign=4096, IODepth=64, RWMixRead=30, RandPercent=0, NumJobs=2,
                                 RunTime=3600, StartDelay=0, LoopCnt=20)
        perfitem2.save()
        perfcase1 = PerfTestCase(CaseName="fiotest1", Level="BASIC", CaseType="IOPS", TIID=perfg1)
        perfcase1.save()
        perfcase2 = PerfTestCase(CaseName="fiotest2", Level="FULL", CaseType="IOPS", TIID=perfg1)
        perfcase2.save()
        perfcaseitem1 = PerfItemInCase(TIID=perfitem1, TCID=perfcase1)
        perfcaseitem1.save()
        perfcaseitem2 = PerfItemInCase(TIID=perfitem1, TCID=perfcase2)
        perfcaseitem2.save()
        perfcaseitem3 = PerfItemInCase(TIID=perfitem2, TCID=perfcase1)
        perfcaseitem3.save()
        perfref1 = PerfRefTarget(Project="taiplus", RefUnit="IOPS", RefVal=10000, IICID=perfcaseitem1)
        perfref1.save()
        comptestitem = CompTestItem(Name="comp1", Description="comp1 test", OSRequired="linux", Automated=True, ToolName="fio",
                                    ToolVersion="3.1", ToolPath="c:\\tools", ToolParam="--size = 200G", Comments="")
        comptestitem.save()
        comptestcase = CompTestCase(Name="compcase1", SupportOS="linux", OSVersion="centos7.2", HWBrandReq="hwband",
                                    HWModelReq="hwmodel", HWReqLables="hwlabel", DUTReqLables="dutlabel", TTID=comptestitem)
        comptestcase.save()
        compprj = CompProject(Project="tai", Status="todo")
        compprj.save()
        compprj.TCID.set([comptestcase])
        self.c = Client()

    def testAddRefSpec(self):
        """
        """
        url = "/testcase/api/func_test/add_refspec/"
        data_dic ={"data": { "FileName":"NVME", 
                            "Standard":"False", 
                            "Version":"224", 
                            "FilePath":"C:\\Spec\\Nvme"
                            }
                }
        add_obj = CaseFuncsBase(url, data_dic, 3, self.c, self.assertEqual, self.assertTrue)
        add_obj.data_dic = {
                            "data": { "FileName":"NVME", 
                                    "Standard":"True", 
                                    "Version":"3.0", 
                                    "FilePath":"C:\\Spec\\Nvme"
                                    }
                        }
        res_data = add_obj.sendCmd()
        self.assertEqual(res_data["code"], 5)
#         self.assertEqual(eval(res_data)["data"], 3)
#         self.assertEqual(eval(res_data)["code"], 0)
         
    def testAddTestPoint(self):
        """
        """
        url = "/testcase/api/func_test/add_testpoint/"
        data_dic ={"data": { "TestDesc":"readoutofrange", 
                            "SelectFrom":"bbadfad", 
                            "PageNo":"30", 
                            "SpecAndPoint":"1,2"
                            }
                }
        obj = CaseFuncsBase(url, data_dic, 4, self.c, self.assertEqual, self.assertTrue)
        #constraints check
        obj.data_dic ={"data": 
                            { "TestDesc":"basicread", 
                             "SelectFrom":"bbadfad", 
                             "PageNo":"30", 
                             "SpecAndPoint":"1,2"
                            }
                       }
        res_data = obj.sendCmd()
        self.assertEqual(res_data["code"], 5)
  
    def testAddCaseDesc(self):
        """
        """
        url = "/testcase/api/func_test/add_testcase/"
        data_dic ={"data": { "CaseName":"write2", 
                            "Description":"writeoutofrange", 
                            "CaseAndPoint":"2"
                            }
                }
        CaseFuncsBase(url, data_dic, 3, self.c, self.assertEqual, self.assertTrue)
        
    def testUpdateCaseStep(self):
        """
        """
        #update
        url = "/testcase/api/func_test/mod_casestep/"
        data_dic ={"data": { "CaseName":"write1", 
                            "Step"    : "1",
                            "StepType":"PRE", 
                            "StepDesc":"read with address out of range",
                            "ExpectRslt":"fail"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
#          resp = self.c.post(url, data_dic, content_type="application/json")
#          res_data = resp.content
#          print(str(resp.content, encoding='utf-8'))
#          self.assertTrue(b'"code": 0' in res_data)
#          self.assertTrue(b' "data": true' in res_data)
        #add
        data_dic2 ={"data": { "CaseName":"write1", 
                             "Step"    : "4",
                             "StepType":"MAIN", 
                             "StepDesc":"write with uecc",
                             "ExpectRslt":"fail"
                             }
                 }
        CaseFuncsBase(url, data_dic2, None, self.c, self.assertEqual, self.assertTrue)       
   
    def testUpdateCaseVersion(self):
        """
        """
        url = "/testcase/api/func_test/mod_caseversion/"
        data_dic ={"data": { "CaseName":"write1", 
                            "Version"    : "1.2",
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
        
    def testUpdateCaseSrtInfo(self):
        """
        """
        url = "/testcase/api/func_test/mod_casestrinfo/"
        data_dic ={"data": { "CaseName":"write1", 
                            "ScriptName"    : "featureread.py",
                            "ScriptPath"    : "l2",
                            "ScriptParams"  : "--cap 2000",
                            "Author"        : "xiaowangjian"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
        
    def testUpdateCaseOwnership(self):
        """
        """
        url = "/testcase/api/func_test/mod_caseowner/"
        data_dic ={"data": { "CaseName":"write1", 
                            "Owner"    : "xuhui",
                            "BackupOwner"    : "xuhui"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
    
    def testUpdateCaseProject(self):
        """
        """
        url = "/testcase/api/func_test/mod_caseproject/"
        data_dic ={"data": { "CaseName":"write1", 
                            "Project"    : "mogan",
                            "Status"    : "ready"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
            
        url = "/testcase/api/func_test/mod_caseproject/"
        data_dic ={"data": { "CaseName":"write1", 
                            "Project"    : "TaiPlus",
                            "Status"    : "ready"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
    
    def testUpdateCaseCategory(self):
        """
        """
        url = "/testcase/api/func_test/mod_casecategory/"
        data_dic ={"data": { "CaseName":"write1", 
                            "Automated"    : "False",
                            "Importance"   : "300",
                            "Level"        : "L1",
                            "Category"     : "MRT",
                            "Subcategory"  : "M"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
        
    def testUpdateCaseLabels(self):
        """
        """
        url = "/testcase/api/func_test/mod_caselabel/"
        data_dic ={"data": { "CaseName":"write1", 
                            "Labels"    : "uttest"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
    
    def testUpdateCaseDepInfo(self):
        """
        """
        url = "/testcase/api/func_test/mod_casedepinfo/"
        data_dic ={"data": { "CaseName":"write1", 
                            "HWRequired"    : "uthw",
                            "SWRequired"    : "utsw",
                            "VSRequired"    : "utvs",
                            "DrvSupported"  : "utdrive",
                            "OSSupported"   : "utos",
                            "OEMSupported"  : "utoem",
                            "SKUSupported"  : "utsku"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
       
    def testGetCaseScriptInfo(self):
        """
        """
        url = "/testcase/api/func_test/get_casescript/"
        data_dic ={"data": { "CaseName":"read1"
                            }
                    }
        expect_data = {'CaseName': 'read1', 'ScriptName': 'basicread.py', 
                       'ScriptPath': 'ibm-l2/dataTransfer', 'ScriptParams': '--doPdb True'}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
    
    def testGetCaseSrtOwner(self):
        """
        """
        url = "/testcase/api/func_test/get_caseowner/"
        data_dic ={"data": { "CaseName":"read1"
                            }
                          }
        expect_data = {'Owner': 'cuimei', 'BackupOwner': 'xuhui'}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
     
    def testGetCaseDetailedInfo(self):
        """
        """
        url = "/testcase/api/func_test/get_casedetail/"
        data_dic ={"data": { "CaseName":"read1"
                            }
                          }
        expect_data = {'id': 1, 'CaseName': 'read1', 'Description': 'basic read', 'ScriptName': 'basicread.py',
                       'ScriptPath': 'ibm-l2/dataTransfer', 'ScriptParams': '--doPdb True', 'Version': '1.0', 
                       'Author': 'cuimei', 'Owner': 'cuimei', 'BackupOwner': 'xuhui', 'Automated': True, 'Importance': 20, 
                       'Level': 'L2', 'Category': 'BCI', 'Subcategory': 'M', 'Labels': 'test', 'HWRequired': 'hwread', 
                       'SWRequired': 'sw', 'VSRequired': 'Y', 'DrvSupported': 'drive', 'OSSupported': 'windows', \
                       'OEMSupported': 'lenovo', 'SKUSupported': '8160'}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
    
    def testGetCaseStepInfo(self):
        """
        """
        url = "/testcase/api/func_test/get_casestep/"
        data_dic ={"data": { "CaseName":"read1"
                            }
                          }
        expect_data = [{'id': 1, 'Step': '1', 'StepType': 'MAIN', 'StepDesc': 'write some data', 'ExpectRslt': 'pass'},
                       {'id': 2, 'Step': '2', 'StepType': 'MAIN', 'StepDesc': 'read and compare data', 'ExpectRslt': 'pass'}]
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
        
    def testGetCaseTestPoints(self):
        """
        """
        url = "/testcase/api/func_test/get_casepoint/"
        data_dic ={"data": { "CaseName":"read1"
                            }
                          }
        expect_data = [{'id': 1, 'TestDesc': 'basicread', 'SelectFrom': 'fdafdafdaf', 'PageNo': 10, 'FileName': 'UFS', 'Version': '3.0'}, 
                       {'id': 1, 'TestDesc': 'basicread', 'SelectFrom': 'fdafdafdaf', 'PageNo': 10, 'FileName': 'NVME', 'Version': '3.0'}, 
                       {'id': 2, 'TestDesc': 'basicwrite', 'SelectFrom': 'bbbbb', 'PageNo': 10, 'FileName': 'NVME', 'Version': '3.0'}]
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
   
    def testGetCaseProjectInfo(self):
        """
        """
        url = "/testcase/api/func_test/get_caseprjinfo/"
        data_dic ={"data": { "CaseName":"read1"
                            }
                          }
        expect_data = [{'Project': 'TaiPlus', 'Status': 'TODO'}]
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
       
    def testGetProjectCases(self):
        """
        """
        url = "/testcase/api/func_test/get_prjcaselist/"
        data_dic ={"data": { "Project":"TaiPlus",
                            "Status"  : "TODO"
                            }
                          }
        expect_data = [{'id': 1, 'Project': 'TaiPlus', 'CaseName': 'read1'}, 
                       {'id': 2, 'Project': 'TaiPlus', 'CaseName': 'write1'}]
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
           
        url = "/testcase/api/func_test/get_prjcaselist/"
        data_dic ={"data": { "Project":"TaiPlus",
                            "Status"  : "TODO",
                            "Depends" : "hwread"
                            }
                          }
        expect_data = [{'id': 1, 'Project': 'TaiPlus', 'CaseName': 'read1'}]
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
  
    def testAddPerfTestItem(self):
        """
        """
        url = "/testcase/api/perf_test/add_item/"
        data_dic ={"data": { "ItemName":"utAddPerfTestItem", 
                            "CheckPoint":"SSS", 
                            "AccessPercent":"30", 
                            "BlockSize":"4096",
                            "BlockAlign":"4096",
                            "IODepth"   : "256",
                            "RWMixRead" : "100",
                            "RandPercent" :"100",
                            "NumJobs"   : "32",
                            "RunTime"   : "3600",
                            "StartDelay": "0",
                            "LoopCnt"   : "3"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
  
    def testAddPerfGlobal(self):
        """
        """
        url = "/testcase/api/perf_test/add_global/"
        data_dic ={"data": { "GlobalName":"utGlobal", 
                            "MaxIOSize":"100", 
                            "Offset":"0", 
                            "NeedPurge":"False",
                            "Need2XFillDriver":"True",
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
  
    def testAddPerfTestCase(self):
        """
        """
        url = "/testcase/api/perf_test/add_case/"
        data_dic ={"data": { "CaseName":"utTestCase", 
                            "Level":"COMMON", 
                            "CaseType":"LATENCY", 
                            "GlobalName":"fio",
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
  
    def testAddItemIntoCase(self):
        """
        """
        url = "/testcase/api/perf_test/add_item_case/"
        data_dic ={"data": { "CaseName":"fiotest1", 
                            "ItemName":"test1", 
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
  
    def testAddItemRefVal(self):
        """
        """
        url = "/testcase/api/perf_test/add_ref/"
        data_dic ={"data": { "CaseName":"fiotest2", 
                            "ItemName":"test1", 
                            "Project" :"taiplus",
                            "RefUnit" : "IOPS",
                            "RefVal"  : "100"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
      
    def testGetCaseTestItems(self):
        """
        """
        url = "/testcase/api/perf_test/get_item/"
        data_dic ={"data": { "CaseName":"fiotest1"
                            }
                          }
        expect_data =  [{'ItemName': 'test1'}, {'ItemName': 'test2'}]
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
      
    def testGetPerfGlobal(self):
        """
        """
        url = "/testcase/api/perf_test/get_global/"
        data_dic ={"data": { "GlobalName":"fio"
                            }
                          }
        expect_data =  {'GlobalName': 'fio', 'MaxIOSize': 100, 'Offset': 0, 'NeedPurge': True, 'Need2XFillDriver': False}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
      
    def testGetTestCase(self):
        """
        """
        url = "/testcase/api/perf_test/get_case/"
        data_dic ={"data": { "CaseName":"fiotest1"
                            }
                          }
        expect_data =  {'GlobalName': 'fio', 'CaseName': 'fiotest1', 'CaseType': 'IOPS'}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
      
    def testGetCaseItem(self):
        """
        """
        url = "/testcase/api/perf_test/get_case_item/"
        data_dic ={"data": { "ItemName":"test1"
                            }
                          }
        expect_data =  {'ItemName': 'test1', 'CheckPoint': 'FOB', 'AccessPercent': 100, 'BlockSize': 4096, 'BlockAlign': 4096, 'IODepth': 64, 
                        'RWMixRead': 30, 'RandPercent': 0, 'NumJobs': 2, 'RunTime': 3600, 'StartDelay': 0, 'LoopCnt': 10}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
      
    def testGetItemRefVal(self):
        """
        """
        url = "/testcase/api/perf_test/get_ref/"
        data_dic ={"data": {"CaseName":"fiotest1",
                            "ItemName":"test1",
                            "Project" : "taiplus"
                            }
                          }
        expect_data =  {'RefUnit': 'IOPS', 'RefVal': '10000'}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
      
    def testFindPerfTestCase(self):
        """
        """
        url = "/testcase/api/perf_test/find_case/"
        data_dic ={"data": {"Level":"BASIC",
                            }
                          }
        expect_data =   [{'CaseName': 'fiotest1'}]
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
      
    def testAddToolTestItem(self):
        """
        """
        url = "/testcase/api/comp_test/add_item/"
        data_dic ={"data": { "Name":"comp2", 
                            "Description":"comp2 test", 
                            "OSRequired":"linux", 
                            "Automated":"True",
                            "ToolName":"benchmark",
                            "ToolVersion":"3.2",
                            "ToolPath" : "c:\\tools",
                            "ToolParam": "--percent 10",
                            "Comments" : "uttest"
                            }
                }
        obj = CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
      
    def testAddToolTestCase(self):
        """
        """
        url = "/testcase/api/comp_test/add_case/"
        data_dic ={"data": { "Name":"comp2case",
                            "SupportOS":"linux", 
                            "OSVersion":"fedora7.2", 
                            "HWBrandReq":"hwbrand2",
                            "HWModelReq":"hwmodel2",
                            "HWReqLables":"hwlabel2",
                            "DUTReqLables" :"dutlabel2",
                            "TTID" : "1",
                            }
                }
        obj = CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)    
 
    def testUpdateToolProjectStatus(self):
        """
        """
        url = "/testcase/api/comp_test/mod_prj_status/"
        data_dic ={"data": { "CaseName":"compcase1", 
                            "Project"  : "tai",
                            "Status"  :"ready"
                            }
                }
        CaseFuncsBase(url, data_dic, None, self.c, self.assertEqual, self.assertTrue)
 
    def testGetToolTestCase(self):
        """
        """
        url = "/testcase/api/comp_test/get_case/"
        data_dic ={"data": {"Name":"compcase1",
                            }
                          }
        expect_data =  {'Name': 'compcase1', 'SupportOS': 'linux', 'OSVersion': 'centos7.2', 'HWBrandReq': 'hwband', 'HWModelReq': 'hwmodel', 
                        'HWReqLables': 'hwlabel','DUTReqLables': 'dutlabel'}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)
 
    def testGetToolTestItem(self):
        """
        """
        url = "/testcase/api/comp_test/get_item/"
        data_dic ={"data": {"Name":"comp1",
                            }
                          }
        expect_data =  {'Name': 'comp1', 'Description': 'comp1 test', 'OSRequired': 'linux', 'Automated': True, 'ToolName': 'fio',
                        'ToolVersion': '3.1', 'ToolPath': 'c:\\tools', 'ToolParam': '--size = 200G', 'Comments': ''}
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)

    def testFindCompProjTestCases(self):
        """
        """
        url = "/testcase/api/comp_test/find_prj_case/"
        data_dic ={"data": {"Project":"all",
                            }
                          }
        expect_data =   [{'Name': 'compcase1'}]
        CaseFuncsBase(url, data_dic, expect_data, self.c, self.assertEqual)

class CaseFuncsBase(object):
    """
            测试 function的基类
    """
    def __init__(self, url, data_dic, expect_data, c, checkFun, assertFun=None, runCheck=True):
        """
        """
        self.url = url
        self.data_dic = data_dic
        self.expect_data = expect_data
        self.c       = c
        self.checkFun = checkFun
        self.assertFun = assertFun
        print("url:%s" % self.url)
        if runCheck:
            self.funTest()
    
    def sendCmd(self):
        """
        """
        resp = self.c.post(self.url, self.data_dic, content_type="application/json")
        res_data = json.loads(str(resp.content, encoding='utf-8'))
        print(res_data)
        return res_data
        
    def funTest(self):
        """
        """
        res_data = self.sendCmd()
        #check return code
        self.checkFun(res_data["code"], 0)
        print(res_data["data"])
        #check return result
        if self.expect_data is None:
            if self.assertFun is None:
                RuntimeError("Need input assert function")
            else:
                self.assertFun(res_data["data"])
        else:
            self.checkFun(res_data["data"], self.expect_data)