from django.db import models

class DUTInfo(models.Model):
    """
    DUT基本信息表
    """
    DeviceType = models.CharField('设备类型', max_length=16,null=True,blank=True)
    Manufacture = models.CharField('厂商', max_length=16,null=True,blank=True)
    SerialNum = models.CharField('设备序列号', max_length=64,unique=True)
    ModelNum = models.CharField('型号', max_length=64,null=True,blank=True)
    EUI = models.CharField('EUI信息', max_length=16,null=True,blank=True)
    Interface = models.CharField('接口类型', max_length=16,null=True,blank=True) #AIC/U.2/M.2
    ProductName = models.CharField('产品名称', max_length=16,null=True,blank=True)
    RawCapacity = models.CharField('物理容量',max_length=16,null=True,blank=True)
    UserCapacity = models.CharField('用户可见容量',max_length=16,null=True,blank=True)
    Manufactured = models.DateTimeField('生产年月	',null=True,blank=True)
    Status = models.CharField('当前设备状态', max_length=16,null=True,blank=True) #Idle,Busy,Debug,Unplugged
    Notes = models.TextField('备注',null=True,blank=True)
    HostName = models.CharField('当前SSD所在Host机器名称', max_length=32, null=True, blank=True)
    SlotID = models.ForeignKey(verbose_name='当前SSD在Host机器的卡槽位置',to='SlotInfo',on_delete=models.SET_NULL,null=True, blank=True)
    GroupID = models.IntegerField('当前组编号',default=255)
    Tags = models.CharField('当前标签',max_length=64,null=True,blank=True)
    FWLoaderRev = models.CharField('当前FWLoader版本',max_length=16,null=True,blank=True)
    GoldenFWRev = models.CharField('当前Golden版本',max_length=16,null=True,blank=True)
    FWRev = models.CharField('当前FW版本',max_length=16,null=True,blank=True)

    def __str__(self):
        return self.SerialNum

class DUTFW(models.Model):
    '''
    FW变更信息表
    '''
    DUTID = models.ForeignKey(verbose_name='对应dut', to='DUTInfo', on_delete=models.CASCADE)
    Changed = models.DateTimeField('发生改变的日期时间', auto_now_add=True)
    Operator = models.CharField('操作者',max_length=32,null=True,blank=True)
    FWLoaderRev = models.CharField('Bootloader版本号',max_length=16,null=True,blank=True)
    FWRev = models.CharField('FW版本号',max_length=16,null=True,blank=True)
    GoldenFWRev = models.CharField('GoldenFW版本号',max_length=16,null=True,blank=True)

    def __str__(self):
        return self.FWRev

class DUTHost(models.Model):
    '''
    Host/Solt变更信息表
    '''
    DUTID = models.ForeignKey(verbose_name='对应dut', to='DUTInfo', on_delete=models.CASCADE)
    Changed = models.DateTimeField('发生改变的日期时间', auto_now_add=True)
    Operator = models.CharField('操作者',max_length=32,null=True,blank=True)
    HostName = models.CharField('SSD所在Host机器的名称', max_length=32, null=True, blank=True)
    SlotID = models.IntegerField('SSD在Host机器的卡槽位置', null=True, blank=True)

    def __str__(self):
        return self.HostName

class DUTMonitor(models.Model):
    '''
    DUT健康监控记录表
    '''
    DUTID = models.ForeignKey(verbose_name='对应dut', to='DUTInfo', on_delete=models.CASCADE)
    Changed = models.DateTimeField('发生改变的日期时间', auto_now_add=True)
    Operator = models.CharField('操作者',max_length=32,null=True,blank=True)
    CurrentPower = models.FloatField('设备当前功耗	',null=True,blank=True)
    T1 = models.IntegerField('温度#1',null=True,blank=True)
    T2 = models.IntegerField('温度#2',null=True,blank=True)
    AvgAging = models.IntegerField('NAND擦写次数',null=True,blank=True)
    HostWrtten = models.IntegerField('Host端数据写入量',null=True,blank=True)
    HostRead = models.IntegerField('Host端数据读取量',null=True,blank=True)
    PowerCycles = models.IntegerField('PowerCycle次数',null=True,blank=True)
    PowerOnHours = models.IntegerField('上电总时间长',null=True,blank=True)
    UnsafeShutdowns = models.IntegerField('异常掉电次数',null=True,blank=True)
    MediaErrNum = models.IntegerField('数据相关错误次数',null=True,blank=True)
    ErrLogNum = models.IntegerField('ErrLog Entries Count',null=True,blank=True)
    PCIE = models.CharField('PCIE信息',max_length=16,null=True,blank=True)
    Vendor_INFO1 = models.CharField('VendorDefinedInfo#1',max_length=32,null=True,blank=True)
    Vendor_INFO2 = models.CharField('VendorDefinedInfo#2',max_length=32,null=True,blank=True)
    Vendor_INFO3 = models.CharField('VendorDefinedInfo#3',max_length=32,null=True,blank=True)

class DUTGrp(models.Model):
    '''
    Grp/tags变更信息表
    '''
    DUTID = models.ForeignKey(verbose_name='对应dut', to='DUTInfo', on_delete=models.CASCADE)
    Changed = models.DateTimeField('发生改变的日期时间', auto_now_add=True)
    Operator = models.CharField('操作者',max_length=32,null=True,blank=True)
    GroupID = models.IntegerField('组编号	',default=255)
    Tags = models.CharField('标签',max_length=64,null=True,blank=True)

    def __str__(self):
        return self.Tags

class HostInfo(models.Model):
    '''
    主机信息表
    '''
    HostName = models.CharField('主机名称',max_length=32,unique=True)
    Manufacture = models.CharField('品牌',max_length=16,null=True,blank=True)
    DeviceModel = models.CharField('产品型号',max_length=32,null=True,blank=True)
    DeviceType = models.CharField('设备类型',max_length=10,null=True,blank=True) #PC，Server，AIO
    MotherBoard = models.CharField('主板信息',max_length=32,null=True,blank=True)
    CPUType = models.CharField('CPU类型',max_length=32,null=True,blank=True)
    NumOfCPU = models.IntegerField('标配CPU数量',null=True,blank=True)
    MaxCPUNum = models.IntegerField('最大CPU数量',null=True,blank=True)
    CPUCores = models.IntegerField('CPU核数',null=True,blank=True)
    DRAMType = models.CharField('内存类型', max_length=16, null=True, blank=True)
    DRAMSize = models.CharField('内存大小', max_length=16, null=True, blank=True)
    MaxDRAMSize = models.CharField('最大内存大小', max_length=16, null=True, blank=True)
    MAC = models.CharField('网卡MAC地址', max_length=16, null=True, blank=True)
    IPV4Addr = models.CharField('IP地址', max_length=16, null=True, blank=True)
    NICType = models.CharField('网络接口卡', max_length=16, null=True, blank=True) #100M,1000M,10GB
    WIFISupported = models.BooleanField('是否支持wifi',default=False)
    IPV4WIFI = models.CharField('WIFI的IP地址', max_length=16, null=True, blank=True)
    MaxSATASlot = models.IntegerField('最大可插入SATA SSD数量',null=True,blank=True)
    MaxAICSlot = models.IntegerField('最大可插入AIC SSD数量',null=True,blank=True)
    MaxU2Slot = models.IntegerField('最大可插入U.2 SSD数量',null=True,blank=True)
    JoininDate = models.DateTimeField('加入测试池时间',null=True,blank=True)
    Status = models.CharField('主机状态',max_length=16,default='IDEL') #IDEL,BUSY,BAD,RETIRED

    def __str__(self):
        return self.HostName

class SlotInfo(models.Model):
    '''
    SSD Slot信息表
    '''
    SlotID = models.IntegerField('Slot位置序号')
    HostID = models.ForeignKey(verbose_name='对应主机',to='HostInfo',on_delete=models.CASCADE)
    Status = models.CharField('状态',max_length=16,null=True,blank=True) #Good，Bad
    Interface = models.CharField('接口类型',max_length=16,null=True,blank=True) #SATA，PCIe，U.2

    def __str__(self):
        return self.SlotID

    class Meta:
        unique_together = ('SlotID', 'HostID',)

class HostOS(models.Model):
    '''
    主机OS变更信息表
    '''
    HostID = models.ForeignKey(verbose_name='对应主机', to='HostInfo', on_delete=models.CASCADE)
    Changed = models.DateTimeField('发生改变的日期时间', auto_now_add=True)
    Operator = models.CharField('操作者', max_length=32, null=True, blank=True)
    OSType = models.CharField('操作系统类型', max_length=16, null=True, blank=True) #Windows, Linux, MacOS
    OSVersion = models.CharField('操作系统版本', max_length=32, null=True, blank=True)

    def __str__(self):
        return self.OSVersion

class HostDriver(models.Model):
    '''
    主机驱动信息记录表
    '''
    OSID = models.ForeignKey(verbose_name='对应的OS', to='HostOS', on_delete=models.CASCADE)
    Changed = models.DateTimeField('发生改变的日期时间', auto_now_add=True)
    Operator = models.CharField('操作者', max_length=32, null=True, blank=True)
    Hardware = models.CharField('驱动对应的硬件名称', max_length=32, null=True, blank=True)
    DriverName = models.CharField('驱动包的名称', max_length=32, null=True, blank=True)
    DriverVersion = models.CharField('驱动的版本信息', max_length=32, null=True, blank=True)

    def __str__(self):
        return self.DriverName

    # class Meta:
    #     unique_together = ('OSID', 'Hardware',)

class HostMonitor(models.Model):
    '''
    主机健康状态监控记录表
    '''
    HostID = models.ForeignKey(verbose_name='对应主机', to='HostInfo', on_delete=models.CASCADE)
    Changed = models.DateTimeField('发生改变的日期时间', auto_now_add=True)
    Operator = models.CharField('操作者', max_length=32, null=True, blank=True)
    CPUUsage = models.IntegerField('CPU使用率	',null=True,blank=True)
    RAMUsage = models.IntegerField('RAM使用率	',null=True,blank=True)
    DISKUsage = models.IntegerField('DISK使用百分比',null=True,blank=True)
    NetworkConnection = models.BooleanField('',default=False)
    NetworkUsage = models.IntegerField('Network带宽百分比',null=True,blank=True)
    TotalProcesses = models.IntegerField('当前进程数',null=True,blank=True)

class HostSoftware(models.Model):
    '''
    主机软件工具记录表
    '''
    OSID = models.ForeignKey(verbose_name='对应的OS', to='HostOS', on_delete=models.CASCADE)
    Changed = models.DateTimeField('发生改变的日期时间', auto_now_add=True)
    Operator = models.CharField('操作者', max_length=32, null=True, blank=True)
    ToolName = models.CharField('工具名称', max_length=32, null=True, blank=True)
    ToolVer = models.CharField('工具版本信息', max_length=16, null=True, blank=True)

    def __str__(self):
        return self.ToolName

    # class Meta:
    #     unique_together = ('OSID', 'ToolName',)

class ScriptSrtInfo(models.Model):
    '''
    ScriptSrtInfo信息表
    '''
    PKGID = models.ForeignKey(verbose_name='对应的包', to='ScriptPackage', on_delete=models.CASCADE)
    SrtName = models.CharField('Script名称', max_length=32, null=True, blank=True)
    GitRepo = models.CharField('Script对应的Repo信息', max_length=128, null=True, blank=True)
    GitBranch = models.CharField('Script对应的Branch信息', max_length=64, null=True, blank=True)
    GitCommitID = models.CharField('Script对应的CommitID信息', max_length=16, null=True, blank=True)

    def __str__(self):
        return self.SrtName

class ScriptPackage(models.Model):
    '''
    ScriptPackage表
    '''
    PkgName = models.CharField('Package (Folder) Name', max_length=64, unique=True)
    Project = models.CharField('项目名称', max_length=32, null=True, blank=True)
    Date = models.DateTimeField('Checkout的日期时间', auto_now_add=True)
    PkgPath = models.CharField('Package路径', max_length=255, null=True, blank=True)
    Labels = models.CharField('标签', max_length=64, null=True, blank=True)

    def __str__(self):
        return self.PkgName

class FWBinary(models.Model):
    '''
    FWBinary信息表
    '''
    PKGID = models.ForeignKey(verbose_name='对应的包', to='FWPackage', on_delete=models.CASCADE)
    BinaryType = models.CharField('BIN档类型', max_length=16, null=True, blank=True) #GOLDEN,SIMPLE,CONNECT,AGING,BOOTFW,OEMFW
    GitRepo = models.CharField('FW对应的Repo信息', max_length=128, null=True, blank=True)
    GitBranch = models.CharField('FW对应的Branch信息', max_length=64, null=True, blank=True)
    GitCommitID = models.CharField('FW对应的CommitID信息', max_length=16, null=True, blank=True)
    BinaryName = models.CharField('BIN档名称',max_length=64,null=True,blank=True)

    def __str__(self):
        return self.BinaryName

class FWPackage(models.Model):
    '''
    FWPackage表
    '''
    PkgName = models.CharField('Package (Folder) Name', max_length=64, unique=True)
    Project = models.CharField('项目名称', max_length=32, null=True, blank=True)
    External = models.BooleanField('是否是对外发布的版本',default=False)
    Date = models.DateTimeField('BIN打包日期时间', auto_now_add=True)
    PkgType = models.CharField('Package类型', max_length=16, null=True, blank=True) #DEBUG，AUTO，TEST，MP，OEM
    PkgPath = models.CharField('Package路径', max_length=255, null=True, blank=True)
    Labels = models.CharField('标签', max_length=64, null=True, blank=True)

    def __str__(self):
        return self.PkgName

class FWRelease(models.Model):
    '''
    FWPackage版本信息表
    '''
    Name = models.CharField('发布名称',max_length=64,unique=True)
    PKGID = models.ForeignKey(verbose_name='对应的包', to='FWPackage', on_delete=models.CASCADE)
    TRName = models.CharField('TestRun Name', max_length=32, null=True, blank=True)
    Date = models.DateTimeField('发布的时间', auto_now_add=True)
    Version = models.CharField('发布的版本信息', max_length=32, null=True, blank=True)

    def __str__(self):
        return self.Name