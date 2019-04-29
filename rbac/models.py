from django.db import models

# Create your models here.
class UserProfile(models.Model):
    """
    用户信息
    """
    name = models.CharField('姓名', max_length=32)
    email = models.EmailField('邮箱',default='')
    phone = models.CharField('座机', max_length=32)
    mobile = models.CharField('手机', max_length=32)
    roles = models.ManyToManyField(verbose_name='具有的所有角色', to="Role", blank=True)
    is_admin = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.name

class AdminInfo(models.Model):
    """
    用户登录
    """
    user = models.OneToOneField("UserProfile",on_delete=models.CASCADE)
    username = models.CharField('用户名', max_length=32,unique=True)
    password = models.CharField('密码', max_length=32)

class Role(models.Model):
    """
    role
    """
    title = models.CharField(verbose_name='角色名',max_length=32, unique=True)
    permissions = models.ManyToManyField(verbose_name='具有的所有权限', to='Permission', blank=True)

    class Meta:
        verbose_name_plural = "用户组表"

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题',max_length=32)
    url = models.CharField(verbose_name="含正则URL",max_length=64)

    class Meta:
        verbose_name_plural = "权限表"

    def __str__(self):
        return self.title

class BusinessUnit(models.Model):
    """
    主机组(部门)
    """
    name = models.CharField(verbose_name='主机组名称', max_length=64, unique=True)
    roles = models.ManyToManyField(verbose_name="对应用户组",to=Role,blank=True)

    class Meta:
        verbose_name_plural = "主机组表"

    def __str__(self):
        return self.name

