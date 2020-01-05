from django.db import models

# Create your models here.

import datetime
import os

from utils.basemodel import CreateUpdateMixin, MediaMixin

'''
class Uploadir(object):
    def __init_self, date):
        open('/static/media/' + date, 'w', encoding='uft-8')
'''


class FillBankType(CreateUpdateMixin):
    atypechoice = (
        (0, 'text_con'),
        (1, 'image_con'),
        (2, 'audio_con'),
    )
    cur_type = models.SmallIntegerField(choices=atypechoice, default=0, verbose_name='答题类型', help_text='答题类型')
    sub = models.ManyToManyField('FillbankSub')

    class Meta:
        verbose_name_plural = '填空题类型'
        verbose_name = '填空题类型'


class ChoiceType(CreateUpdateMixin):
    atypechoice = (
        (0, 'text_con'),
        (1, 'image_con'),
        (2, 'audio_con'),
    )
    cur_type = models.SmallIntegerField(choices=atypechoice, default=0, verbose_name='答题类型', help_text='答题类型')
    sub = models.ManyToManyField('ChoiceSub')

    class Meta:
        verbose_name_plural = '选择题类型'
        verbose_name = '选择题类型'


class FillbankSub(CreateUpdateMixin):
    title = models.CharField('填空-题目', unique=True, max_length=100, null=False, help_text='题目')
    answer = models.CharField(max_length=100, null=False, verbose_name='答案', help_text='答案')

    image_url = models.CharField(max_length=100, null=True, verbose_name='图片', help_text='图片')
    audio_url = models.CharField(max_length=100, null=True, verbose_name='音频', help_text='音频')
    source = models.CharField(max_length=64, null=True, verbose_name='题目来源', help_text='题目来源')
    perSore = models.SmallIntegerField(null=False, default=1, verbose_name='本题分数', help_text='本题分数')

    class Meta:
        verbose_name_plural = '填空题'
        verbose_name = '填空题'


class ChoiceSub(CreateUpdateMixin):
    title = models.CharField(max_length=100, unique=True, null=False, verbose_name='选择-题目', help_text='题目')
    answer = models.CharField(max_length=100, null=False, verbose_name='答案', help_text='答案')
    radio1 = models.CharField(max_length=32, null=True, verbose_name='选项一', help_text='选项一')
    radio2 = models.CharField(max_length=32, null=True, verbose_name='选项二', help_text='选项二')
    radio3 = models.CharField(max_length=32, null=True, verbose_name='选项三', help_text='选项三')
    radio4 = models.CharField(max_length=32, null=True, verbose_name='选项四', help_text='选项四')

    image_url = models.CharField(max_length=100, null=True, verbose_name='图片', help_text='图片')
    audio_url = models.CharField(max_length=100, null=True, verbose_name='音频', help_text='音频')
    source = models.CharField(max_length=64, null=True, verbose_name='题目来源', help_text='题目来源')
    perSore = models.SmallIntegerField(null=False, default=1, verbose_name='本题分数', help_text='本题分数')

    class Meta:
        verbose_name_plural = '选择题'
        verbose_name = '选择题'


'''
class Subject(models.Model):
    date = str(datetime.datetime.now().date()
    # print(time.strftime('%Y-%m')

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
        return models.Model.__new__(*args, **kwargs)
'''


class TopicInfo(models.Model):
    qsize = models.SmallIntegerField(null=False, default=0, verbose_name='题库大小', help_text='题库大小')
    qname = models.CharField(null=False, max_length=20, unique=True, verbose_name='题库名', help_text='题库名')
    qselect = models.SmallIntegerField(null=False, default=0, verbose_name='选择题数', help_text='选择题数')
    qfillblank = models.SmallIntegerField(null=False, default=0, verbose_name='填空题数', help_text='填空题数')
    qucount = models.SmallIntegerField(null=False, default=0, verbose_name='参与人次', help_text='参与人次')
    qhasmatch = models.SmallIntegerField(null=False, default=0, verbose_name='已出比赛数', help_text='已出比赛数')

    fbinfo = models.ManyToManyField(to='FillbankSub')
    chinfo = models.ManyToManyField(to='ChoiceSub')
    aid = models.ForeignKey(to='userapp.AuthUser', to_field='id', on_delete=models.CASCADE)
    # qtype = models.ForeignKey(to='TopicType', to_field='id', on_delete=models.CASCADE)
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
    qtype = models.SmallIntegerField(choices=topichoice, default=7, null=False, verbose_name='题库类型', help_text='题库类型')

    class Meta:
        verbose_name_plural = '题库信息'
        verbose_name = '题库信息'


'''
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
    topictype = models.SmallIntegerField(choices=topichoice, default=7, null=False, verbose_name='题库类型', help_text='题库类型')

    class Meta:
        verbose_name_plural = '题库类型'
        verbose_name = '题库类型'
'''
