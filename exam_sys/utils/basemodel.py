import os
from django.db import models
# from django.utils.translation import gettext_lazy as _  # 引入延迟加载方法，只有在视图渲染时该字段才会呈现出翻译值
from TimeConvert import TimeConvert as tc
# https://pypi.org/project/TimeConvert/1.4.1/
from django.conf import settings

class CreateUpdateMixin(models.Model):
    '''模型创建和更新时间戳'''

    status = models.BooleanField('状态', default=True, help_text='状态', db_index=True)  # 状态值
    create_at = models.DateTimeField('创建时间', auto_now_add=True, editable=True, help_text='创建时间')
    update_at = models.DateTimeField('更新时间', auto_now=True, editable=True, help_text='更新时间')

    class Meta:
        abstract = True  # 抽象类，仅用于继承用，不会生成表


class MediaMixin(models.Model):
    # image = models.CharField(max_length=100, null=True, help_text=_('图片链接'), verbose_name=_('图片链接'))
    image = models.CharField(max_length=100, null=True, help_text='图片链接', verbose_name='图片链接')
    audio = models.CharField(max_length=256, null=True, help_text='音频链接', verbose_name='音频链接')

    class Meta:
        abstract = True

'''
    @property
    def media(self):
        return {
            'image': self.image,
            'audio': self.audio,
        }
'''


class ModelHelper(object):
    def upload_img_path(self, filename):
        '''上传图片的默认路径'''
        # usonpython.JPG
        return 'images/{ym}/{stamp}.{ext}'.format(
            ym=tc.local_string(format='%Y-%m'),
            stamp=tc.local_timestamp(),
            # ext=filename.split('.')[1].lower(),
            ext=os.path.splitext(filename)[1].lower(),
        )

    def upload_file_path(self, filename):
        '''
        上传模板文件
        :param filename: 模板文件名
        :return: 文件存放路径
        '''
        return "templatefile/{ym}/".format(
            ym=tc.local_string(format='%Y-%m')
        ) + filename
__mh = ModelHelper()
img_path = __mh.upload_img_path  # 暂时不传参数
file_path = __mh.upload_file_path
