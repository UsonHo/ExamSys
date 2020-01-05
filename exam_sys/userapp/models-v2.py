from django.db import models

from utils.basemodel import CreateUpdateMixin, MediaMixin, ModelHelper
from django.utils.translation import gettext_lazy as _

# Create your models here.

class RegUser(CreateUpdateMixin):
    uemail = models.EmailField(max_length=64, null=False, unique=True, db_index=True, verbose_name=_('邮箱'), help_text=_('邮箱'))
    uname = models.CharField(max_length=10, null=False, unique=True, verbose_name=_('用户名'), help_text=_('用户名'))
    upasswd = models.CharField(max_length=32, null=False, verbose_name=_('密码'), help_text=_('密码'))
    isauth = models.BooleanField(default=0, null=True, verbose_name=_('是否认证'), help_text=_('是否认证'))

    # 是否注销账户信息
    isdelete = models.BooleanField(default=0, null=True, verbose_name=_('是否已删除'), help_text=_('是否已删除'))


class AuthUser(CreateUpdateMixin):
    oemail = models.EmailField(max_length=64, null=False, unique=True, verbose_name=_('邮箱'), help_text=_('邮箱'))
    oname = models.CharField(max_length=32, null=False, unique=True, verbose_name=_('公司名称'), help_text=_('公司名称'))
    oreluname = models.CharField(max_length=5, null=False, verbose_name=_('真实姓名'), help_text=_('真实姓名'))
    oumobile = models.DecimalField(max_digits=11, decimal_places=0, null=False, verbose_name=_('认证手机号'), help_text=_('认证手机号'))
    otypechoice = (
        (0, '互联网IT'),
        (1, '金融'),
        (2, '房地产/建筑'),
        (3, '贸易/零售/物流'),
        (4, '教育/传媒/广告'),
        (5, '服务业'),
        (6, '市场/销售'),
        (7, '人事/财务/行政'),
        (8, '其他'),
    )
    otype = models.IntegerField(choices=otypechoice, default=4, null=False, verbose_name=_('公司类型'), help_text=_('公司类型'))
    userinfo = models.OneToOneField(to='RegUser', to_field='id', on_delete=models.CASCADE)


class UserProfile(CreateUpdateMixin):
    uaddr = models.CharField(max_length=128, null=True, verbose_name=_('用户住址'), help_text=_('用户住址'))
    uschool = models.CharField(max_length=20, null=True, verbose_name=_('毕业院校'), help_text=_('毕业院校'))
    ugenderchoice = (
        (0, '男'),
        (1, '女'),
    )
    ugender = models.IntegerField(choices=ugenderchoice, default=0, null=False, verbose_name=_('性别'), help_text=_('性别'))
    uage = models.IntegerField(null=True, verbose_name=_('年龄'), help_text=_('年龄'))
    umobile = models.CharField(max_length=11, null=True, verbose_name=_('手机号'), help_text=_('手机号'))
    uweixin = models.CharField(max_length=20, null=True, verbose_name=_('微信号'), help_text=_('微信号'))
    uidentify = models.CharField(max_length=18, null=True, verbose_name=_('身份证号'), help_text=_('身份证号'))

    # 不需要,仅仅用在比赛结果记录中
    # baseinfo = models.OneToOneField(to='RegUser', to_field='id', on_delete=models.CASCADE)
