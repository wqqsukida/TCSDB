from django.db import models
from django.db.models.lookups import StartsWith

# Create your models here.
class ReferSpec(models.Model):
    """
    reference spec information
    """
    FileName    = models.CharField(max_length=40, default='NVME', verbose_name="Protocol Type")
    Standard    = models.BooleanField()
    Version     = models.CharField(max_length=10)
    FilePath    = models.CharField(max_length=80)   
    class Meta:
        verbose_name_plural = "spec reference"
        constraints = [models.UniqueConstraint(fields=['FileName', "Standard", "Version"], name='unique_refer_spec')]

    def __str__(self):
        return (self.FileName+":" +self.Version)
    
class TestPoint(models.Model):
    """
    test point information
    """
    TestDesc     = models.CharField(max_length=80, unique=True)
    SelectFrom   = models.TextField(max_length=200)
    PageNo       = models.IntegerField()
    SpecAndPoint = models.ManyToManyField(ReferSpec, blank=True, related_name="spec_point", verbose_name="specAndTestpoint")
    class Meta:
        verbose_name_plural = "test point"

    def __str__(self):
        return self.TestDesc

class TestCaseDetail(models.Model):
    """
    Detial for test cases.
    """
    LevelChoice  = (('L0' , "UnitTest"),
                    ('L1' , "FeatureTest"),
                    ('L2', "ProtocolTest"),
                    ('L3', "PerformanceTest"),
                    ('L4', "SystemTest"),
                    ('L5', "CompitibleTest"),
                    ('L6', "SelfTest"),
                    ('L7', "ProductionTest")
                         )
    CaseName     = models.CharField(max_length=40, unique=True)
    Description  = models.CharField(max_length=80)
    ScriptName   = models.CharField(max_length=80, blank=True)
    ScriptPath   = models.CharField(max_length=80, blank=True)
    ScriptParams = models.CharField(max_length=80, blank=True)
    Version      = models.CharField(max_length=10, blank=True)
    Author       = models.CharField(max_length=20, blank=True)
    Owner        = models.CharField(max_length=20, blank=True)
    BackupOwner  = models.CharField(max_length=20, blank=True)
    Automated    = models.BooleanField(null=True)
    Importance   = models.IntegerField(null=True)
#     Level        = models.CharField(choices=LevelChoice, max_length=20, default='L1')
    Level        = models.CharField(max_length=20, blank=True)
    Category     = models.CharField(max_length=30, blank=True)
    Subcategory  = models.CharField(max_length=10, blank=True)
    Labels       = models.CharField(max_length=40, blank=True)
    HWRequired   = models.CharField(max_length=40, blank=True)
    SWRequired   = models.CharField(max_length=40, blank=True)
    VSRequired   = models.CharField(max_length=40, blank=True)
    DrvSupported = models.CharField(max_length=40, blank=True)
    OSSupported  = models.CharField(max_length=40, blank=True)
    OEMSupported = models.CharField(max_length=40, blank=True)
    SKUSupported = models.CharField(max_length=40, blank=True)
    CaseAndPoint = models.ManyToManyField(TestPoint, related_name="case_point", verbose_name="tcAndTestPoint") 

    class Meta:
        verbose_name_plural = "test case detail"

    def __str__(self):
        return self.CaseName

class TestProject(models.Model):
    """
    test project information
    """
    StatusChoice  = (('TODO', "NotDone"),
                    ('DESIGN' , "Doing"),
                    ('READY', "Done"),
                    ('STABLE', "Stable"),
                    ('DEBUG', "Havebug"),
                    ('OBSOLETE', "obsolte"),
                         )
    Project      = models.CharField(max_length=20)
    Status       = models.CharField(choices=StatusChoice, max_length=10)
    TID          = models.ManyToManyField(TestCaseDetail, related_name="case_project", verbose_name="caseProject")
    class Meta:
        verbose_name_plural = "test project"

    def __str__(self):
        return self.Project
    
class CaseStep(models.Model):
    """
    test case steps
    """
    StepChoice  = (('PRE', "BeforeTest"),
                    ('POST' , "AfterTest"),
                    ('MAIN', "Test"),)
    Step         = models.IntegerField()
    StepType     = models.CharField(choices=StepChoice, max_length=10)
    StepDesc     = models.CharField(max_length=80)
    ExpectRslt   = models.CharField(max_length=80)
    TID          = models.ForeignKey(TestCaseDetail, related_name="case_step", on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "test case step"

    def __str__(self):
        return self.StepDesc