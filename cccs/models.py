from django.db import models

class TestCycle(models.Model):
    '''
    TestCycle表
    '''
    Project = models.CharField('项目名称', max_length=32, null=True, blank=True)
    CycleName = models.CharField('TestCycle名称', max_length=32)
    CycleLevel = models.CharField('Cycle等级', max_length=16, null=True, blank=True) # DRT,MRT,BRT,SMK,BCI,BVT,SVT
    Status = models.CharField('Cycle状态',max_length=16,null=True,blank=True) # ACTIVE，INACTIVE
    Created = models.DateTimeField('创建日期',auto_now_add=True)
    TriggeredTotal = models.IntegerField('共计被触发次数',default=0)
    LastTriggered = models.DateTimeField('最近一次触发时间	', null=True,blank=True)

    def __str__(self):
        return self.CycleName

class TestPlan(models.Model):
    '''
    TestPlan表
    '''
    CaseName = models.CharField('TestCase名称', max_length=64)
    CycleID = models.ForeignKey(verbose_name='TestCycle ID', to='TestCycle',
                                on_delete=models.SET_NULL,null=True, blank=True)
    Created = models.DateTimeField('创建日期',auto_now_add=True)
    Status = models.CharField('Case在Plan中的状态',max_length=16,null=True,blank=True) # ACTIVE，INACTIVE
    LoopCnt = models.IntegerField('重复运行次数',null=True,blank=True)

    def __str__(self):
        return self.CaseName

class TestRun(models.Model):
    '''
    TestRun表
    '''
    TestRunName = models.CharField('TestRun名称', max_length=32, unique=True)
    TriggerTime = models.DateTimeField('计划触发时间',null=True,blank=True)
    StartTime = models.DateTimeField('开始时间',null=True,blank=True)
    EndTime = models.DateTimeField('结束时间',null=True,blank=True)
    Status = models.CharField('状态', max_length=16, default='NOTSTART')  # NOTSTART，RUNING，CANCELED，FINISHED
    TCID = models.ForeignKey(verbose_name='TestCycle ID', to='TestCycle',
                             on_delete=models.SET_NULL,null=True, blank=True)
    JIRAID = models.CharField('对应的JIRA ID',max_length=16,null=True,blank=True)
    DUTGRPID = models.IntegerField('DUT Group ID',null=True,blank=True)
    FWPkgName = models.CharField('FW Package Name', max_length=16, null=True, blank=True)
    SrtPkgName = models.CharField('Script Package Name', max_length=16, null=True, blank=True)
    Comments = models.TextField('备注信息	',null=True, blank=True)

class TestAction(models.Model):
    '''
    操作记录表
    '''
    ActionChoice = (
        (1,"TestCycle"),
        (2,"TestPlan"),
    )
    ActionType = models.IntegerField(choices=ActionChoice,default=1)
    OriginalVal = models.CharField('原值',max_length=16, null=True, blank=True)
    NewVal = models.CharField('新值',max_length=16, null=True, blank=True)
    ActionTime = models.DateTimeField('操作日期时间',auto_now_add=True)
    ActionOP = models.CharField('操作者',max_length=32,null=True,blank=True)
    PlanID = models.ForeignKey(to='TestPlan',on_delete=models.SET_NULL,null=True, blank=True)
    CycleID = models.ForeignKey(to='TestCycle',on_delete=models.SET_NULL,null=True, blank=True)
