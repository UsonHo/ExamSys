from django import forms
from topicapp.models import TopicInfo
from userapp.models import AuthUser
from django.forms.models import ModelChoiceField
from django.core.exceptions import ValidationError
from topicapp.config import USERID_ERROR, TOPICTYPE_ERROR, SETTIME_ERROR, ENDTIME_ERROR, MATCHNAME_ERROR, MULTIPLE_ERROR
import time
from .models import MatchConfig


class ConfigForm(forms.Form):
    qtype = forms.IntegerField(  # 因为是写在内存中的元组，不能通过ModelChoiceField查询数据库展示，前端展示:<option value=qtype[0]>qtype[1]</option>
        initial=7,  # 补充：因为不是外键关联，不能用ModelChoiceField,通过clean_qtype二次验证
        widget=forms.widgets.Select(
            choices=TopicInfo.topichoice,
        )
    )
    qid = forms.ModelChoiceField(
        queryset=TopicInfo.objects.values('id'),
        to_field_name='id',
    )

    mname = forms.CharField(
        max_length=20,
        min_length=6,
        error_messages={
            'max_length': '太长了，你不累吗？',
            'min_length': '太短了，别人怎么看',
            'required': '比赛名称不能空空如也',
        }
    )
    organame = forms.CharField(
        max_length=32,
        error_messages={
            'required': '机构名称被篡改，你妈还想再看你一眼，快...',
            'max_length': '你...你祖宗叫你呢？听...'
        }
    )
    aid = ModelChoiceField(  # ForeignKey,字段名可以不同,但必须与前端提交的name保持一致
        # 先判断用户提交的id是否在数据库查询集中,否则报错：不在选项列表中
        queryset=AuthUser.objects.values('id', 'oname'),
        to_field_name='id',
        # 出现异常：code = invalid_choice
    )  # 字段验证时候，取值跟字段定义的顺序还是有关系的
    score = forms.IntegerField(
        min_value=1,
        max_value=1000,
        error_messages={
            'required': '总分数不设置，你考个毛线啊',
            'min_value': '总分数这么低，你想下地狱啊？',
            'max_value': '总分数这么高，你这么喜欢天堂吗？',
        }
    )
    topicount = forms.IntegerField(
        min_value=1,
        max_value=50,
        error_messages={
            'required': '题目都不设置，你考狗啊',
            'min_value': '有你这么出题的吗?滚？',
            'max_value': '你想头顶开花吗',
        }
    )
    stime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],  # 注意是个列表
        error_messages={
            'required': '你是怎么绕过前端验证滴,老子看到你了，别跑',
            'invalid': '看，你后面是什么？',
        }
    )
    etime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        error_messages={
            'required': '师傅，闪开，妖精来了',
            'invalid': '看，你踩到了狗屎',
        }
    )
    mtime = forms.IntegerField(
        min_value=5,
        max_value=250,
        error_messages={
            'required': '把你头剁了，猪食倒进去可以吗？那也要给我1妙钟',
            'min_value': '太快了，爽吗？',
            'max_value': '只有累死的牛，没有耕坏的地',
        }
    )
    mregular = forms.CharField(
        max_length=100,
        min_length=5,
        error_messages={
            'required': '非人即畜',
            'min_length': '你这太短了',
            'max_length': '你这太长了',
        }
    )
    extrainfo = forms.BooleanField(
        required=False,
        initial=0,
    )
    choicefield = forms.CharField(
        required=False,
    )
    otherinfo = forms.CharField(
        required=False,
    )

    def clean_mname(self):
        mname = self.cleaned_data['mname']
        obj = MatchConfig.objects.filter(mname=mname).first()
        if obj:
            raise ValidationError('比赛名重复', code=MATCHNAME_ERROR)
        return mname

    def clean_aid(self):
        obj = AuthUser.objects.filter(**self.cleaned_data['aid']).first()
        # 再根据数据库中查询集的组合结果,判断用户提交的另一字段是否相等
        if 'organame' in self.cleaned_data:
            if obj.oname != self.cleaned_data['organame']:
                raise ValidationError('用户信息不正确或者被伪造', code=USERID_ERROR)
        return self.cleaned_data['aid']

    def clean_qtype(self):
        for item in TopicInfo.topichoice:
            # print(item[0], self.cleaned_data['qtype'], type(self.cleaned_data['qtype'])) int
            if item[0] == self.cleaned_data['qtype']:
                return self.cleaned_data['qtype']
        raise ValidationError('题库类型选择被篡改', code=TOPICTYPE_ERROR)

    def clean_stime(self):
        cur_time = time.time()

        post_stime = self.cleaned_data['stime']
        # 获取到的时间需要手动格式化一下
        formated = post_stime.strftime('%Y-%m-%d %H:%M')
        # 格式化字符串转元组
        tup = time.strptime(formated, "%Y-%m-%d %H:%M")
        # 元组转时间戳
        valid_time = time.mktime(tup)

        if cur_time + 300 > valid_time:
            raise ValidationError('我已看到你不是人，篡改了js验证，请离开', code=SETTIME_ERROR)
        return self.cleaned_data['stime']

    def clean_etime(self):
        end_time = self.cleaned_data['etime'].strftime('%Y-%m-%d %H:%M')
        tup = time.strptime(end_time, '%Y-%m-%d %H:%M')
        valid_time = time.mktime(tup)

        start_time = self.cleaned_data['stime'].strftime('%Y-%m-%d %H:%M')
        tup2 = time.strptime(start_time, '%Y-%m-%d %H:%M')
        prevalid_time = time.mktime(tup2)

        if prevalid_time + 86400 > valid_time:
            raise ValidationError('你是黑...狗, 不, 反正不是人', code=ENDTIME_ERROR)
        return self.cleaned_data['etime']

    # def clean_extrainfo(self):
    #     istrue = self.cleaned_data['extrainfo']
    #     if not istrue:
    #         return self.cleaned_data['extrainfo']

    def clean_choicefield(self):
        import json
        if len(json.loads(self.cleaned_data['choicefield'])) > 5:
            raise ValidationError('贪心总要还的', code=MULTIPLE_ERROR)
        return self.cleaned_data['choicefield']

    def clean_otherinfo(self):
        import json
        if len(json.loads(self.cleaned_data['otherinfo'])) > 5:
            raise ValidationError('贪心总要还的', code=MULTIPLE_ERROR)
        return self.cleaned_data['otherinfo']

    # def clean(self):
    #     print(self.cleaned_data)
    #     return self.cleaned_data
