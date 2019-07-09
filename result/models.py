from django.db import models

# Create your models here.
class ResultSummary(models.Model):
    '''
    功能测试结果概要
    '''
    TRName = models.CharField('TestRun名称',max_length=32,blank=True,null=True)
    TotalCases = models.IntegerField('测试用例总数',default=0)
    PassCnt = models.IntegerField('Pass用例总数',default=0)
    FailCnt = models.IntegerField('Fail用例总数',default=0)
    AbortCnt = models.IntegerField('Abort用例总数',default=0)
    SkipCnt = models.IntegerField('Skip用例总数',default=0)
    CPassCnt = models.IntegerField('Conditional Pass用例总数',default=0)
    NotRunCnt = models.IntegerField('NotRun用例总数',default=0)
    SrtLogRoot = models.CharField('脚本Log的根目录', max_length=128, blank=True, null=True)
    FWLogRoot = models.CharField('FWLog的根目录', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.TRName

class ResultDetail(models.Model):
    '''
    功能测试结果详情
    '''
    TRID = models.ForeignKey(verbose_name='ResultSummary ID',to='ResultSummary',on_delete=models.CASCADE)
    TCName = models.CharField('TestCase名称',max_length=64,blank=True,null=True)
    Result = models.CharField('用例结果信息',max_length=16,blank=True,null=True) #PASS，CPASS，FAIL，ABORT，SKIP，NOTRUN
    StartTime = models.DateTimeField('用例开始时间	',blank=True,null=True)
    EndTime = models.DateTimeField('用例结束时间',blank=True,null=True)
    SerialNum = models.CharField('DUT SN', max_length=64, blank=True, null=True)
    ScriptLog = models.CharField('脚本Log的相对路径+文件名', max_length=128, blank=True, null=True)
    FWLog = models.CharField('FWLog的相对路径+文件名', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.TCName

class ResultFailure(models.Model):
    '''
    功能测试失败详情
    '''
    RRID = models.ForeignKey(verbose_name='ResultDetail ID', to='ResultDetail', on_delete=models.CASCADE)
    JIRAID = models.CharField('',max_length=16,blank=True,null=True)
    FailureKept = models.BooleanField('是否有保留现场	',default=False)
    DebugLog = models.CharField('DebugDumpLog的相对路径+文件名',max_length=128,blank=True,null=True)
    DbgInfo1 = models.CharField('调试信息1,eg:DUT所对应的窗口信息',max_length=64,blank=True,null=True)
    DbgInfo2 = models.CharField('调试信息2,eg:DUT所对应的SSD串口信息',max_length=64,blank=True,null=True)


class PerfResultSummary(models.Model):
    '''
    性能测试结果概要
    '''
    TRName = models.CharField('TestRun名称',max_length=32,blank=True,null=True)
    TotalCases = models.IntegerField('用例总数',blank=True,null=True)
    TotalItems = models.IntegerField('用例项总数',blank=True,null=True)
    RunCases = models.IntegerField('已经完成用例数',blank=True,null=True)
    RunItems = models.IntegerField('已经完成项数',blank=True,null=True)
    LogRoot = models.CharField('日志根目录', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.TRName

class PerfResultDetail(models.Model):
    '''
    性能 测试 结果详情
    '''
    TRID = models.ForeignKey(verbose_name='PerfResultSummary ID',to='PerfResultSummary',on_delete=models.CASCADE)
    TCName = models.CharField('TestCase名称',max_length=64,blank=True,null=True)
    StratTime = models.DateTimeField('用例开始时间	',blank=True,null=True)
    EndTime = models.DateTimeField('用例结束时间',blank=True,null=True)
    SerialNum = models.CharField('DUT SN', max_length=64, blank=True, null=True)
    ScriptLog = models.CharField('脚本Log的相对路径+文件名', max_length=128, blank=True, null=True)
    FWLog = models.CharField('FWLog的相对路径+文件名', max_length=128, blank=True, null=True)
    StatLog = models.CharField('StatLog的相对路径+文件名', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.TCName

class PerfResultItem(models.Model):
    '''
    性能 测试项 结果具体信息
    '''
    RRID = models.ForeignKey(verbose_name='PerfResultDetail ID', to='PerfResultDetail', on_delete=models.CASCADE)
    ItemName = models.CharField('TestItem名称',max_length=32,blank=True,null=True)
    Unit = models.CharField('度量单位',max_length=16,blank=True,null=True) #MBPS,IOPS,MS,US,%
    Value = models.IntegerField('测量值',blank=True,null=True)
    RawData = models.TextField('采样数据(压缩)',blank=True,null=True)

    def __str__(self):
        return self.ItemName