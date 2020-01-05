from django.db import models
import datetime

from utils.basemodel import CreateUpdateMixin, MediaMixin, ModelHelper


# Create your models here.

class RegUser(CreateUpdateMixin):
    uemail = models.EmailField(max_length=64, null=False, unique=True, db_index=True, verbose_name='邮箱', help_text='邮箱')
    uname = models.CharField(max_length=10, null=False, unique=True, verbose_name='用户名', help_text='用户名')
    upasswd = models.CharField(max_length=32, null=False, verbose_name='密码', help_text='密码')
    isauth = models.BooleanField(default=0, null=True, verbose_name='是否认证', help_text='是否认证')

    # 是否注销账户信息
    isdelete = models.BooleanField(default=0, null=True, verbose_name='是否已删除', help_text='是否已删除')

    # 用户其他信息
    uaddr = models.CharField(max_length=128, null=True, verbose_name='用户住址', help_text='用户住址')
    uschool = models.CharField(max_length=20, null=True, verbose_name='毕业院校', help_text='毕业院校')
    ugender = models.CharField(max_length=5, null=True, verbose_name='性别', help_text='性别')
    uage = models.IntegerField(null=True, verbose_name='年龄', help_text='年龄')
    umobile = models.CharField(max_length=11, null=True, verbose_name='手机号', help_text='手机号')
    uweixin = models.CharField(max_length=20, null=True, verbose_name='微信号', help_text='微信号')
    uid = models.CharField(max_length=18, null=True, verbose_name='身份证号', help_text='身份证号')

    class Meta:
        verbose_name = '普通用户'
        verbose_name_plural = '普通用户'


class AuthUser(CreateUpdateMixin):
    oemail = models.EmailField(max_length=64, null=False, unique=True, verbose_name='邮箱', help_text='邮箱')
    oname = models.CharField(max_length=32, null=False, unique=True, verbose_name='公司名称', help_text='公司名称')
    oreluname = models.CharField(max_length=20, null=False, verbose_name='真实姓名', help_text='真实姓名')
    oumobile = models.DecimalField(max_digits=11, decimal_places=0, null=False, verbose_name='认证手机号', help_text='认证手机号')
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
    otype = models.IntegerField(choices=otypechoice, default=4, null=False, verbose_name='公司类型', help_text='公司类型')
    userinfo = models.OneToOneField(to='RegUser', to_field='id', on_delete=models.CASCADE, related_name='authuser')

    class Meta:
        verbose_name = '机构用户'
        verbose_name_plural = '机构用户'


'''
class UserProfile(CreateUpdateMixin):
    uaddr = models.CharField(max_length=128, null=True, verbose_name='用户住址', help_text='用户住址')
    uschool = models.CharField(max_length=20, null=True, verbose_name='毕业院校', help_text='毕业院校')
    uname = models.CharField(max_length=20, null=True, verbose_name='答题者', help_text='答题者')
    uemail = models.CharField(max_length=64, null=True, verbose_name='邮箱', help_text='邮箱')
    ugender = models.CharField(max_length=5, null=True, verbose_name='性别', help_text='性别')
    uage = models.IntegerField(null=True, verbose_name='年龄', help_text='年龄')
    umobile = models.CharField(max_length=11, null=True, verbose_name='手机号', help_text='手机号')
    uweixin = models.CharField(max_length=20, null=True, verbose_name='微信号', help_text='微信号')
    uid = models.CharField(max_length=18, null=True, verbose_name='身份证号', help_text='身份证号')

    # 不需要,仅仅用在比赛结果记录中
    # baseinfo = models.OneToOneField(to='RegUser', to_field='id', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '用户其他信息'
        verbose_name_plural = '用户其他信息'
'''


# 第一种: 存储在sqlite/mysql数据库中
class EmailVerify(CreateUpdateMixin):
    # 邮箱及验证码
    code = models.CharField(unique=True, max_length=20, verbose_name="验证码", null=False, blank=False)
    email = models.EmailField(unique=True, max_length=50, verbose_name="邮箱", null=False, blank=False)

    # 验证类型
    send_type = models.CharField(
        max_length=10, verbose_name="验证码类型",
        choices=(('register', "注册"), ('forget', "找回密码"),), default="forget",
    )
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.datetime.now())

    class Meta:
        verbose_name_plural = "邮箱验证码"
        verbose_name = verbose_name_plural

    def __unicode__(self):
        return "{0}({1})".format(self.code, self.email)

# 第二种: 存储在redis数据库中
