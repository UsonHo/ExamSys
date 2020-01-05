from django.db import models

from django.utils.translation import gettext_lazy as _
from utils.basemodel import CreateUpdateMixin, MediaMixin
# Create your models here.

class MatchConfig(CreateUpdateMixin):
    mname = models.CharField(max_length=20, null=False, unique=True, verbose_name=_('比赛名称'), help_text=_('比赛名称'))
    mtime = models.SmallIntegerField(null=False, verbose_name=_('设置比赛时间'), help_text=_('设置比赛时间'), default=0)
    topicount = models.SmallIntegerField(null=False, verbose_name=_('总题数'), help_text=_('总题数'), default=10)
    score = models.SmallIntegerField(null=False, verbose_name=_('总分数'), help_text=_('总分数'), default=100)
    stime = models.DateTimeField(null=False, verbose_name=_('比赛开始时间'), help_text=_('比赛开始时间'))
    etime = models.DateTimeField(null=False, verbose_name=_('比赛截止时间'), help_text=_('比赛截止时间'))

    # 可选择字段
    uname = models.BooleanField(default=0, null=True, verbose_name=_('用户名'), help_text=_('用户名'))
    uaddr = models.BooleanField(default=0, null=True, verbose_name=_('用户住址'), help_text=_('用户住址'))
    uemail = models.BooleanField(default=0, null=True, verbose_name=_('邮箱'), help_text=_('邮箱'))
    uschool = models.BooleanField(default=0, null=True, verbose_name=_('毕业院校'), help_text=_('毕业院校'))
    ugender = models.BooleanField(default=0, null=True, verbose_name=_('性别'), help_text=_('性别'))
    uage = models.BooleanField(default=0, null=True, verbose_name=_('年龄'), help_text=_('年龄'))
    umobile = models.BooleanField(default=0, null=True, verbose_name=_('手机号'), help_text=_('手机号'))
    uweixin = models.BooleanField(default=0, null=True, verbose_name=_('微信'), help_text=_('微信'))
    uid = models.BooleanField(default=0, null=True, verbose_name=_('身份证号'), help_text=_('身份证号'))

    option_fields = models.TextField(max_length=255, null=True, verbose_name=_('下拉框字段'),
                                     help_text=_('下拉框字段选项配置，#号隔开，每个字段由:h和，号组成。 '
                                                 '如 option1:吃饭，喝水，睡觉#option2:上班，学习，看电影'))

    qinfo = models.ForeignKey(to='topicapp.TopicInfo', to_field='id', on_delete=models.CASCADE)
    auinfo = models.ForeignKey(to='userapp.AuthUser', to_field='id', on_delete=models.CASCADE)

class MatchReport(CreateUpdateMixin):
    statuschoice = (
        (0, '已完成'),
        (1, '未完成'),
        (2, '超时'),
    )
    status = models.IntegerField(choices=statuschoice, default=1, null=False, verbose_name=_('答题状态'), help_text=_('答题状态'))
    question_record = models.CharField(max_length=10000, null=True, verbose_name=_('问题记录'), help_text=_('问题记录'))
    answer_record = models.CharField(max_length=10000, null=True, verbose_name=_('答案记录'), help_text=_('答案记录'))
    stime = models.DateTimeField(null=True, default=0, verbose_name=_('答题开始时间'), help_text=_('答题开始时间'))
    etime = models.DateTimeField(null=True, default=0, verbose_name=_('答题结束时间'), help_text=_('答题结束时间'))
    right_list = models.CharField(max_length=10000, null=True, verbose_name=_('正确题目'), help_text=_('正确的题目'))
    error_list = models.CharField(max_length=10000, null=True, verbose_name=_('错误的题目'), help_text=_('错误的题目'))
    right_count = models.IntegerField(default=0, verbose_name=_('答对总题数'), help_text=_('答对总题数'))
    error_count = models.IntegerField(default=0, verbose_name=_('答错总题数'), help_text=_('答错总题数'))
    question_count = models.IntegerField(default=0, verbose_name=_('总题数'), help_text=_('总题数'))

    usedtime = models.DecimalField(max_digits=2, decimal_places=1, null=False, verbose_name=_('答题用时'), help_text=_('答题用时'))
    resgrade = models.SmallIntegerField(null=False, verbose_name=_('考试成绩'), help_text=_('考试成绩'))

    # Foreign写在多的一方，就是为了实例化时候，少的一方无需实例化多的那方数据，因为根本没有数据可以实例化
    userinfo = models.ForeignKey(to='userapp.UserProfile', to_field='id', on_delete=models.CASCADE)
    baseuser = models.ForeignKey(to='userapp.RegUser', to_field='id', on_delete=models.CASCADE)
