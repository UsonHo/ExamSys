from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
import re
from .models import RegUser
from utils.check_mail import FindPwdSendMail


def email_validate(value):
    email_re = re.compile(r'^[a-z0-9A-Z][.\w]+@[0-9a-zA-Z]+\.[a-zA-Z]+$')
    if not email_re.match(value):
        raise ValidationError('邮箱格式错误')


class FindPwdForm(forms.Form):
    # 第三种验证码-用于找回密码
    captcha = CaptchaField(
        required=True,
        error_messages={
            'required': '验证码不能不写哦',
            'invalid': '验证码错误哦,请重新输入',
        }
    )
    femail = forms.EmailField(
        validators=[email_validate, ],
        required=True,
        error_messages={
            'required': '邮箱必须填写',
        }
    )
    new_passwd = forms.CharField(
        max_length=10,
        min_length=4,
        required=True,
        error_messages={
            'required': '密码必填',
        }
    )
    confirm_passwd = forms.CharField(
        required=True,
        error_messages={
            'required': '密码必填',
        }
    )

    def clean_femail(self):
        email_obj = RegUser.objects.filter(uemail=self.cleaned_data.get('femail')).first()
        if not email_obj:
            raise ValidationError('邮箱未注册', 'invalid')
        return self.cleaned_data['femail']

    def clean_confirm_passwd(self):
        confirm_pwd = self.cleaned_data.get('confirm_passwd')
        if self.cleaned_data.get('new_passwd') != confirm_pwd:
            raise ValidationError('两次密码输入不一致,请重新输入', 'invalid')
        return confirm_pwd

    def clean(self):
        # 发送邮件
        send_status = FindPwdSendMail.send_code_email(self.cleaned_data['femail'], 'forget')
        print("send_status:", send_status)
        if not send_status:
            raise ValidationError('邮件发送失败', 'invalid')
        # return send_status  # 最后不能返回Bool值，它会把这个结果复制给cleaned_data,cleaned_data就你没有数据了
        return self.cleaned_data
