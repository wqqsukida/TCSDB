from django.db import models

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

    def __str__(self):
        return self.FileName

class SpecAndTestPoint(models.Model):
    """
    refer spec and test point relationship
    """
    TPID       = models.IntegerField()
    SpecID     = models.ForeignKey(ReferSpec, related_name="spec_content", verbose_name="spec_id", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "test point and spec relationship"

class TestPoint(models.Model):
    """
    test point information
    """
    TestDesc    = models.CharField(max_length=80)
    SelectFrom  = models.TextField(max_length=200)
    PageNo      = models.IntegerField()
    tpid        = models.OneToOneField(SpecAndTestPoint, related_name="point_content", verbose_name="point_id",  on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "test point"

    def __str__(self):
        return self.TestDesc



