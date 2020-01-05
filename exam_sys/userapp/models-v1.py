from django.db import models

# Create your models here.

class RegUser(models.Model):
    uemail = models.EmailField(max_length=64, null=False)
    uname = models.CharField(max_length=10, null=False)
    upasswd = models.CharField(max_length=32, null=False)
    isauth = models.BooleanField(default=0, null=True)

    regdate = models.DateTimeField(auto_now_add=True)
    savedate = models.DateTimeField(auto_now=True)
    # 是否注销账户信息
    isdelete = models.BooleanField(default=0, null=True)

class AuthUser(models.Model):
    oemail = models.EmailField(max_length=64, null=False)
    oname = models.CharField(max_length=32, null=False)
    oreluname = models.CharField(max_length=5, null=False)
    oumobile = models.DecimalField(max_digits=11, decimal_places=0, null=False)
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
    otype = models.IntegerField(choices=otypechoice, default=4, null=False)
    userinfo = models.OneToOneField(to='RegUser', to_field='id', on_delete=models.CASCADE)

class UserProfile(models.Model):
    uaddr = models.CharField(max_length=128, null=True)
    uschool = models.CharField(max_length=20, null=True)
    ugenderchoice = (
        (0, '男'),
        (1, '女'),
    )
    ugender = models.IntegerField(choices=ugenderchoice, default=0, null=False)
    uage = models.IntegerField(null=True)
    umobile = models.CharField(max_length=11, null=True)
    uweixin = models.CharField(max_length=20, null=True)
    uidentify = models.CharField(max_length=18, null=True)

    # 不需要,仅仅用在比赛结果记录中
    # baseinfo = models.OneToOneField(to='RegUser', to_field='id', on_delete=models.CASCADE)
