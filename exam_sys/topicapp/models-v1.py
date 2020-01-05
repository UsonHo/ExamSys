from django.db import models

# Create your models here.

import datetime
import os

'''
class Uploadir(object):
    def __init__(self, date):
        open('/static/media/' + date, 'w', encoding='uft-8')
'''


class SubjectType(models.Model):
    atypechoice = (
        (0, 'text_con'),
        (1, 'image_con'),
        (2, 'audio_con'),
    )
    atype = models.BooleanField(choices=atypechoice, default=0)
    fillbank = models.ManyToManyField('FillbankSub')
    choice = models.ManyToManyField('ChoiceSub')


class FillbankSub(models.Model):
    title = models.CharField('填空-题目', max_length=100, null=False)
    answer = models.CharField(max_length=100, null=False)
    source = models.CharField(max_length=64, null=True)


class ChoiceSub(models.Model):
    title = models.CharField('选择-题目', max_length=100, null=False)
    answer = models.CharField(max_length=100, null=False)
    radio1 = models.CharField(max_length=32, null=True)
    radio2 = models.CharField(max_length=32, null=True)
    radio3 = models.CharField(max_length=32, null=True)
    radio4 = models.CharField(max_length=32, null=True)
    source = models.CharField(max_length=64, null=True)


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
    qsize = models.SmallIntegerField(null=False)
    qname = models.CharField(null=False, max_length=20)
    qselect = models.SmallIntegerField(null=False, default=0)
    qfillblank = models.SmallIntegerField(null=False, default=0)
    qucount = models.SmallIntegerField(null=False, default=0)
    qhasmatch = models.SmallIntegerField(null=False, default=0)

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
    topictype = models.SmallIntegerField(choices=topichoice, default=7, null=False)
