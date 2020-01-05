from django import forms
from django.forms import widgets
from userapp.models import RegUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re


def idcard(idcode):
    # 加权因子
    weight_factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 对应前17位数字，对应相乘
    # 校验码
    check_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    if len(idcode) != 18 and idcode[0: 17].isdigit():
        raise ValidationError('身份证输入错误', 'invalid')
    last = idcode[17]  # 对最后一位进行校验

    # code = idcode + ""
    seventeen = idcode[0: 17]  # 获取前17位

    # ISO 7064:1983.MOD 11 - 2
    # 判断最后一位校验码是否正确
    num, count = 0, 0
    for s in seventeen:
        num += int(s) * weight_factor[count]
        count += 1

    # 获取余数
    resisue = num % 11
    last_no = check_code[resisue]

    # 格式的正则
    # 正则思路
    # 第一位不可能是0
    # 第二位到第六位可以是0-9
    # 第七位到第十位是年份，所以七八位为19或者20
    # 十一位和十二位是月份，这两位是01-12之间的数值
    # 十三位和十四位是日期，是从01-31之间的数值
    # 十五，十六，十七都是数字0-9
    # 十八位可能是数字0-9，也可能是X
    idcard_patter = re.compile(
        r'[1-9]{1}[0-9]{5}([1]{1}[9]{1}[0-9]{2}|[2]{1}[0]{1}[0,1]{1}[0-9]{1})([0]{1}[1-9]{1}|[1]{1}[0-2]{1})([0]{1}[1-9]{1}|[1,2]{1}[0-9]{1}|[3]{1}[0,1]{1})[0-9]{3}([0-9]{1}|[X]{1})')

    # 判断格式是否正确
    rep_rest = re.match(idcard_patter, idcode).group()
    # print(num, resisue, last_no, last, rep_rest)
    if (not rep_rest) or (last_no != last):
        raise ValidationError('身份证输入错误', 'invalid')


class UserExtraInfoForm(forms.ModelForm):
    uemail = forms.EmailField(
        required=False,
        validators=[RegexValidator(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', '邮箱验证不通过')]
    )
    umobile = forms.CharField(
        required=False,
        validators=[RegexValidator(r'^1[3|5|7|8]{1}[0-9]{9}$', '手机号验证不通过')],
    )
    uid = forms.CharField(
        required=False,
        min_length=18,
        max_length=18,
        validators=[idcard, ],
    )

    # 必须写上，因为fields=[]中没有下面字段的验证，否则经过modelform验证后，下面字段的值将被抛弃
    # 如果fields=[]中有下面字段的验证，就可以不定义，但是又因为是可选字段，所以还是必须写上，required=False
    uname = forms.CharField(
        required=False,
    )
    uage = forms.CharField(
        required=False,
    )
    ugender = forms.CharField(
        required=False,
    )
    uweixin = forms.CharField(
        required=False,
    )
    uaddr = forms.CharField(
        required=False,
    )
    uschool = forms.CharField(
        required=False,
    )

    class Meta:
        model = RegUser
        fields = ['uemail', 'umobile', 'uid', 'uname', 'uage', 'ugender', 'uweixin', 'uaddr', 'uschool']
        # fields = '__all__'
