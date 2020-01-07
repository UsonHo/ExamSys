# 基于django实现
from django.core.mail import send_mail
import random
from userapp.models import EmailVerify
from django.conf import settings
from django.urls import reverse

# import smtplib
# from email.header import Header
# from email.mime.text import MIMEText


def random_code(count=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    codes = ''
    for i in range(count):
        codes += random.choice(chars)
    return codes


def send_code_email(email, send_type):
    # 指定需要发送的邮箱
    # 后台数据库中生成验证码,用于校验
    codes = random_code(16)

    # 保存到数据库中
    email_obj = EmailVerify.objects.filter(email=email).first()
    if not email_obj:
        email_obj = EmailVerify()
        email_obj.email = email
        email_obj.code = codes
    email_obj.send_type = send_type
    email_obj.save()

    # 邮箱验证的用途
    if send_type == 'forget':
        email_title = '找回密码'
        findpwd_url = reverse('findpwd')
        email_body = '请点击下面的链接，来完成您的账号密码重置:http://127.0.0.1:8000{0}?code={1}'\
            .format(findpwd_url, email_obj.code)

        # send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
        return True
    return False
