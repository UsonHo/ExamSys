from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from userapp.models import RegUser
# 对密码进行哈希加密
import hmac


class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        this_checkcode = kwargs.pop('this_request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.checkcode = this_checkcode
        print('我的request:', this_checkcode)

    uname = forms.CharField(
        validators=[RegexValidator(r'^[a-zA-Z][^\W+_]+$', '用户名必须字母开头哦')],
        max_length=10,
        min_length=4,
        required=True,
        error_messages={
            'required': '该字段必填',
            'max-length': '用户名最长10个字符',
            'min-length': '用户名至少需要4个字符',
        }
    )
    upasswd = forms.CharField(
        max_length=32,
        min_length=6,
        required=True,
        error_messages={
            'required': '该字段必填',
            'max-length': '密码最长32个字符',
            'min-length': '密码至少需要6个字符',
        }
    )
    con_passwd = forms.CharField(
        max_length=32,
        min_length=6,
        required=True,
        error_messages={
            'required': '该字段必填',
            'max-length': '密码最长32个字符',
            'min-length': '密码至少需要6个字符',
        }
    )
    uemail = forms.EmailField(
        validators=[RegexValidator(r'^[a-z0-9A-Z][.\w]+@[0-9a-zA-Z]+\.[a-zA-Z]+$', '请输入正确的邮箱格式')],
        required=True,
        error_messages={
            'required': '该字段必填',
        }
    )
    # 第一种:登录,无感滑动验证

    # 第二种验证码-用于注册
    checkcode = forms.CharField(required=True, error_messages={'required': '验证码错误'})


    def clean_uname(self):
        uname = self.cleaned_data.get('uname')
        reg_obj = RegUser.objects.filter(uname=uname).first()
        if reg_obj:
            # self.cleaned_data['uname_error'] = '用户名已被注册'
            raise ValidationError('用户名已被注册', 'invalid')
        return self.cleaned_data['uname']

    def clean_uemail(self):
        uemail = self.cleaned_data.get('uemail')
        reg_obj = RegUser.objects.filter(uemail=uemail).first()

        if reg_obj:
            # self.cleaned_data['uemail_error'] = '邮箱已被注册'
            raise ValidationError('邮箱已被注册', 'invalid')
        return self.cleaned_data['uemail']

    def clean_con_passwd(self):
        upasswd = self.cleaned_data.get('upasswd')
        con_passwd = self.cleaned_data.get('con_passwd')
        if upasswd != con_passwd:
            # self.cleaned_data['con_passwd_error'] = '两次密码输入不一致'
            raise ValidationError("两次密码输入不一致哦", 'invalid')  # 直接存进。errors中
        h_passwd = hmac.new(upasswd.encode('utf-8')).hexdigest()
        self.cleaned_data['upasswd'] = h_passwd
        return self.cleaned_data['upasswd']

    def clean_checkcode(self):
        check_code = self.cleaned_data.get('checkcode')
        print("验证码判断:", check_code)
        if check_code.lower() != self.checkcode.lower():
            raise ValidationError("验证码错误,请重新输入", 'invalid')
        return self.cleaned_data['checkcode']

'''
    def clean_uemail(self):
        upasswd = self.cleaned_data.get('uemail')

    class Meta:
        model = RegUser
        fields = '__all__'
'''
