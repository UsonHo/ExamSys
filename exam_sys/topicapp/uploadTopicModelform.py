import os

from utils.excelHandle import temp_handle
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import widgets

from utils.basemodel import file_path
from .config import TEMPLATE_EXIST_ERROR, TOPICFORMAT_ERROR, TOPICNAME_EXIST_ERROR
from .models import TopicInfo


class UploadTopicModelForm(forms.ModelForm):
    # 以下两种方式都可以写
    # qtype_bak = forms.CharField(
    #     required=False,
    #     initial=7,
    #     widget=widgets.Select(
    #         choices=(
    #             (0, '技术类'),
    #             (1, '教育类'),
    #             (2, '文化类'),
    #             (3, '常识类'),
    #             (4, '地理类'),
    #             (5, '体育类'),
    #             (6, '面试类'),
    #             (7, '热门题库'),
    #         )
    #     )
    # )

    qtype = forms.ChoiceField(
        # initial=7,
        choices=(
            (0, '技术类'),
            (1, '教育类'),
            (2, '文化类'),
            (3, '常识类'),
            (4, '地理类'),
            (5, '体育类'),
            (6, '面试类'),
            (7, '热门题库'),
        ),
        widget=widgets.Select
    )

    qfile = forms.FileField(
        required=True,
        error_messages={
            'required': '您还没有上传题库'
        }
    )

    # (非model中定义或者非前端提交的字段)这里赋值给cleaned_data后views中取值是''，即不是两者当中，而是自定义的字段取值为空''
    # qfilepath = forms.CharField(
    #     required=False
    # )

    # 这里写的字段都是要验证的字段，除非required=False，但是，modelform之外获取其数据就是''，所以不覆写字段和fields
    # fbinfo = forms.ChoiceField(
    #     required=False,
    #     choices=FillbankSub.objects.values_list('id')
    # )
    # chinfo = forms.ChoiceField(
    #     required=False,
    #     choices=ChoiceSub.objects.values_list('id')
    # )

    class Meta:
        model = TopicInfo
        # 我这里前端只传了这四个值，所以只验证四个
        fields = ['qtype', 'qname', 'qfile', 'aid']  # 决定下面字段验证方法的执行顺序
        error_messages = {
            'qname': {
                'max_length': '题库名最大20个字符',
                'require': '题库名必填',
                # 'unique': '题库名重名，请修改'
            }
        }

    def clean_qname(self):
        print("qname:", self.cleaned_data)
        qname_obj = TopicInfo.objects.filter(qname=self.cleaned_data['qname']).first()
        if qname_obj:
            self.cleaned_data['qname'] = False  # 前面字段验证出现异常，后面方法无需验证，我能想到的只有这种办法了，摸索了好半天，self.其他方法都无效
        return self.cleaned_data['qname']

    def clean_qfile(self):
        print("qfile:", self.cleaned_data)
        # print('前面字段验证出现异常，后面方法无需验证，文件保存方法不能再验证', self.cleaned_data['qname'])  # False
        if not self.cleaned_data['qname']:
            raise ValidationError('题库名已存在，请重新修改后提交', code=TOPICNAME_EXIST_ERROR)
        if 'qtype' not in self.cleaned_data:
            raise ValidationError('用户信息被非法')
        topicfile = self.cleaned_data['qfile']
        filepath = os.path.join(settings.MEDIA_ROOT, file_path(topicfile.name))
        if os.path.exists(filepath):
            # 不能使用ValueError,程序报错，并不是报异常
            # raise ValueError('该模板已存在，请重新上传', code=TEMPLATE_EXIST_ERROR)
            raise ValidationError('该模板已存在，请重新上传', code=TEMPLATE_EXIST_ERROR)

        # 判断文件格式是否正确
        if topicfile.name.split('.')[-1] not in ['xls', 'xlsx']:
            raise ValidationError('你上传的模板文件格式不正确', code=TOPICFORMAT_ERROR)

        datedir = filepath.rsplit('/', 1)[0]
        if not os.path.exists(datedir):
            os.mkdir(datedir)

        # 保存文件：
        with open(filepath, 'wb') as fp:
            for line in topicfile.chunks():
                fp.write(line)

        # 解析题库 这里不能使用obj.bfinfo.add() ,可以使用self.cleaned_data['fbinfo'] = id,但多对多必须是列表,所以这里不传，返回列表即可
        backdata = temp_handle(filepath)
        if isinstance(backdata, dict):
            self.cleaned_data.update(backdata)
        else:
            # 如果出现异常，应该把上传的文件删除
            os.remove(filepath)

            raise ValidationError(backdata[0], code=backdata[1])

        # 现在又可以了,因为我取消了类中自定义字段的定义或复写
        # self.cleaned_data['filepath'] = filepath

        return self.cleaned_data['qfile']
