from django.db import models

# Create your models here.

import datetime
import os

from django.utils.translation import gettext_lazy as _
from utils.basemodel import CreateUpdateMixin, MediaMixin

'''
class Uploadir(object):
    def __init__(self, date):
        open('/static/media/' + date, 'w', encoding='uft-8')
'''


class SubjectType(CreateUpdateMixin):
    atypechoice = (
        (0, 'text_con'),
        (1, 'image_con'),
        (2, 'audio_con'),
    )
    atype = models.BooleanField(choices=atypechoice, default=0, verbose_name=_('答题类型'), help_text=_('答题类型'))
    fillbank = models.ManyToManyField('FillbankSub')
    choice = models.ManyToManyField('ChoiceSub')


class FillbankSub(CreateUpdateMixin):
    title = models.CharField(_('填空-题目'), max_length=100, null=False, help_text=_('题目'))
    answer = models.CharField(max_length=100, null=False, verbose_name=_('答案'), help_text=_('答案'))
    source = models.CharField(max_length=64, null=True, verbose_name=_('题目来源'), help_text=_('题目来源'))


class ChoiceSub(CreateUpdateMixin):
    title = models.CharField(max_length=100, null=False, verbose_name=_('选择-题目'), help_text=_('题目'))
    answer = models.CharField(max_length=100, null=False, verbose_name=_('答案'), help_text=_('答案'))
    radio1 = models.CharField(max_length=32, null=True, verbose_name=_('选项一'), help_text=_('选项一'))
    radio2 = models.CharField(max_length=32, null=True, verbose_name=_('选项二'), help_text=_('选项二'))
    radio3 = models.CharField(max_length=32, null=True, verbose_name=_('选项三'), help_text=_('选项三'))
    radio4 = models.CharField(max_length=32, null=True, verbose_name=_('选项四'), help_text=_('选项四'))
    source = models.CharField(max_length=64, null=True, verbose_name=_('题目来源'), help_text=_('题目来源'))


'''
class Subject(models.Model):
    date = str(datetime.datetime.now().date())
    # print(time.strftime('%Y-%m'))

    title = models.CharField('问题-题目', max_length=100, null=False)
    tanswer = models.CharField(max_length=100, null=False)
    tradio1 = models.CharField(max_length=32, null=True)
    tradio2 = models.CharField(max_length=32, null=True)
    tradio3 = models.CharField(max_length=32, null=True)
    tradio4 = models.CharField(max_length=32, null=True)
    tsource = models.CharField(max_length=64, null=True)
    timage = models.ImageField(upload_to='media/' + date, null=True)
    taudio = models.CharField(max_length=256, null=True)

    def __new__(cls, *args, **kwargs):
        if not os.path.exists('/static/media/' + cls.date):
            Uploadir(cls.date)
        return models.Model.__new__(cls, *args)
'''


class TopicInfo(models.Model):
    qsize = models.SmallIntegerField(null=False, default=0, verbose_name=_('题库大小'), help_text=_('题库大小'))
    qname = models.CharField(null=False, max_length=20, unique=True, verbose_name=_('题库名'), help_text=_('题库名'))
    qselect = models.SmallIntegerField(null=False, default=0, verbose_name=_('选择题数'), help_text=_('选择题数'))
    qfillblank = models.SmallIntegerField(null=False, default=0, verbose_name=_('填空题数'), help_text=_('填空题数'))
    qucount = models.SmallIntegerField(null=False, default=0, verbose_name=_('参与人次'), help_text=_('参与人次'))
    qhasmatch = models.SmallIntegerField(null=False, default=0, verbose_name=_('已出比赛数'), help_text=_('已出比赛数'))

    fbinfo = models.ManyToManyField(to='FillbankSub')
    chinfo = models.ManyToManyField(to='ChoiceSub')
    qtype = models.ForeignKey(to='TopicType', to_field='id', on_delete=models.CASCADE)


class TopicType(models.Model):
    topichoice = (
        (0, '技术类'),
        (1, '教育类'),
        (2, '文化类'),
        (3, '常识类'),
        (4, '地理类'),
        (5, '体育类'),
        (6, '面试类'),
        (7, '热门题库'),
    )
    topictype = models.SmallIntegerField(choices=topichoice, default=7, null=False, verbose_name=_('题库类型'), help_text=_('题库类型'))
