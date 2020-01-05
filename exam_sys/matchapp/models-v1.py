from django.db import models

# Create your models here.

class MatchConfig(models.Model):
    mname = models.CharField(max_length=20, null=False)
    mtime = models.SmallIntegerField(null=False)
    topicount = models.SmallIntegerField(null=False)
    score = models.SmallIntegerField(null=False)
    stime = models.DateTimeField(null=False)
    etime = models.DateTimeField(null=False)

    # 可选择字段
    uname = models.BooleanField(default=0, null=True)
    uaddr = models.BooleanField(default=0, null=True)
    uemail = models.BooleanField(default=0, null=True)
    uschool = models.BooleanField(default=0, null=True)
    ugender = models.BooleanField(default=0, null=True)
    uage = models.BooleanField(default=0, null=True)
    umobile = models.BooleanField(default=0, null=True)
    uweixin = models.BooleanField(default=0, null=True)
    uid = models.BooleanField(default=0, null=True)

    qinfo = models.ForeignKey(to='topicapp.TopicInfo', to_field='id', on_delete=models.CASCADE)
    auinfo = models.ForeignKey(to='userapp.AuthUser', to_field='id', on_delete=models.CASCADE)

class MatchReport(models.Model):
    statuschoice = (
        (0, '已完成'),
        (1, '未完成'),
        (2, '超时'),
    )
    status = models.IntegerField(choices=statuschoice, default=1, null=False)
    question_record = models.CharField(max_length=10000, null=True)
    answer_record = models.CharField(max_length=10000, null=True)
    stime = models.DateTimeField()
    etime = models.DateTimeField()
    right_list = models.CharField(max_length=10000, null=True)
    error_list = models.CharField(max_length=10000, null=True)
    right_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    question_count = models.IntegerField(default=0)

    usedtime = models.DecimalField(max_digits=2, decimal_places=1, null=False)
    resgrade = models.SmallIntegerField(null=False)

    # Foreign写在多的一方，就是为了实例化时候，少的一方无需实例化多的那方数据，因为根本没有数据可以实例化
    userinfo = models.ForeignKey(to='userapp.UserProfile', to_field='id', on_delete=models.CASCADE)
    baseuser = models.ForeignKey(to='userapp.RegUser', to_field='id', on_delete=models.CASCADE)
