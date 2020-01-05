from django import forms
# from django.forms.models import ModelChoiceField
from django.forms import widgets
from django.core.exceptions import ValidationError
from userapp.models import AuthUser, RegUser
from django.core.validators import RegexValidator

from django.conf import settings


class OrganModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        login_user = kwargs.pop('login_user', None)
        super(OrganModelForm, self).__init__(*args, **kwargs)
        self.login_user = login_user
        # print("已登录用户：", login_user)

    oemail = forms.EmailField(
        validators=[RegexValidator(r'^[a-z0-9A-Z][.\w]+@[0-9a-zA-Z]+\.[a-zA-Z]+$', '请输入正确的邮箱格式')],
        error_messages={
            'max_length': '邮箱最大长度64个字符',
            'required': '邮箱必填'
        }
    )
    oumobile = forms.CharField(
        validators=[RegexValidator(r'^1[3|5|7|8]{1}[0-9]{9}$', '请输入正确的手机格式')],
        error_messages={
            'required': '联系人手机号必填',
        }
    )

    # userinfo = forms.ChoiceField(
    #     initial=7,
    #     choices=RegUser.objects.values_list('id') form中可以,modelform中不可以
    # )

    otype = forms.CharField(  # 固定内容，model中写在了内容中，如果是需要改动的，就写在数据库中，否则修改后，重启服务，老板伤心
        initial=4,
        widget=widgets.Select(
            choices=(
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
        )
    )
    # 如果想从cleaned_data中获取前端表单字段数据，且字段名不在model中，必须在此定义声明，否则获取到的是None
    m_checkcode = forms.CharField(
        max_length=4,  # 第一次验证
        error_messages={
            'max_length': '短信验证码是您手机号的随机4位',
        }
    )

    class Meta:
        model = AuthUser
        fields = "__all__"
        # exclude = ['userinfo']  # 取消字段后，views中赋值也无法保存到数据库
        error_messages = {
            "__all__": {
            },
            'oname': {
                'max_length': '机构名最大长度32个字符',
            },
            'oreluname': {
                'required': '联系人姓名必填',
            },
        }
        localized_fields = ('create_at', 'update_at')

    '''
    总结：
    在继承forms.ModelForm类时，models中的Onetoone和Manytomany属性会自动转换成ModelChoiceField和ModelMultipleChocieField自动读取数据。
    在ModelForm组件使用中添加数据，可以直接用save()方法,在使用save方法时，如果对象在实例化时有指定第二个关键字参数instance，则为更新操作！

    1、clean_外键:排除字段后，就不执行的，因为该字段不在cleaned_data中
    3、本例通过传入用session得到的用户id，来判断用户是否登录
    '''

    def clean_oemail(self):
        o_obj = AuthUser.objects.filter(oemail=self.cleaned_data['oemail']).first()
        if o_obj:
            raise ValidationError('邮箱已注册，已升级', 'invalid')
        return self.cleaned_data['oemail']

    def clean_m_checkcode(self):  # 第二次验证
        # 短信验证码校验
        print(self.cleaned_data)
        m_code = settings.CONN.get('sms' + self.cleaned_data['oumobile'])
        print("form校验:", m_code, self.cleaned_data.get('m_checkcode'))
        if not m_code:
            self.add_error(None, ValidationError('验证码已过期'))
        if m_code.decode('utf-8') != self.cleaned_data.get('m_checkcode'):
            self.add_error(None, ValidationError('短信验证码错误'))

    def clean(self):
        print('用户状态：', self.login_user)
        if not self.login_user:
            self.add_error(None, ValidationError('用户未登录'))
            # 或者：raise self.add_error(None, ValidationError('用户未登录'))
        # print(type(self.login_user))  # int
        # self.cleaned_data['userinfo_id'] = self.login_user
        return self.cleaned_data
