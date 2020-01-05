# 定义信号
import django.dispatch
from captcha.helpers import captcha_image_url, captcha_audio_url
from captcha.models import CaptchaStore

generate_code = django.dispatch.Signal()

# 注册信号
from django.core.signals import request_finished
from django.dispatch import receiver


@receiver(request_finished)
def code_url():
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)

#   如何能将验证码写到前端页面呢？感觉还是没什么用, 改用js来获取
