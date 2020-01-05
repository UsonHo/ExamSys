from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from userapp.form import RegisterForm
from django.urls import reverse
from .findpwdform import FindPwdForm

from userapp.models import RegUser
import hmac
from exam_sys.settings import captchaClient

# 第二种方式验证码 - 用于注册模态框
from io import BytesIO
from utils.checkcode import create_validate_code

from captcha.helpers import captcha_image_url, captcha_audio_url
from captcha.models import CaptchaStore
from .models import EmailVerify
from django.conf import settings
from .task import del_resetpwd


# Create your views here.


def index(request):
    if request.method == 'GET':
        # 图片验证码
        # hashkey验证码生成的秘钥，image_url验证码的图片地址
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        # Python内置了一个locals()函数，它返回当前所有的本地变量字典
        return render(request, 'userapp/index.html', locals())


def registerHandle(request):
    if request.method == 'POST':
        if request.is_ajax():
            print('是ajax请求')
            reg_obj = RegisterForm(request.POST, this_request=request.session['register_checkcode'])
            if reg_obj.is_valid():
                print('数据合法')
                print(reg_obj.cleaned_data)
                reg_info = {
                    'uname': reg_obj.cleaned_data.get('uname'),
                    'uemail': reg_obj.cleaned_data.get('uemail'),
                    'upasswd': reg_obj.cleaned_data.get('upasswd'),
                }
                RegUser.objects.create(**reg_info)
                reg_obj.cleaned_data['status'] = True
                return JsonResponse(reg_obj.cleaned_data)
            else:
                print('数据不合法')
                return JsonResponse(reg_obj.errors)
        else:
            print('不是ajax请求')
    return redirect('/')


def loginhandle(request):
    if request.method == 'POST':
        if request.is_ajax():
            response = {'field': None, 'status': False, 'error_msg': None}
            uemail = request.POST.get('email')
            user_obj = RegUser.objects.filter(uemail=uemail).first()
            print(user_obj)
            if not user_obj:
                response['error_msg'] = '该邮箱未注册'
                response['field'] = 'email'
                return JsonResponse(response)
            upasswd = user_obj.upasswd
            passwd = request.POST.get('passwd')
            con_upasswd = hmac.new(passwd.encode('utf-8')).hexdigest()
            if upasswd != con_upasswd:
                response['error_msg'] = '密码错误'
                response['field'] = 'passwd'
                return JsonResponse(response)

            # 顶象无感验证码校验
            # captchaClient.setCaptchaUrl("http://cap.dingxiang-inc.com/api/tokenVerify")
            token = request.POST.get('token')
            # print(token)
            response_dx = captchaClient.checkToken(token)
            # print(response_dx['serverStatus'])
            # 确保验证状态是SERVER_SUCCESS，SDK中有容错机制，在网络出现异常的情况会返回通过
            if response_dx['result']:
                # token验证通过，继续其他流程
                print('登录成功')
                response['status'] = True
                request.session['is_login'] = True
                request.session['is_auth'] = user_obj.isauth
                request.session['username'] = user_obj.uname
                request.session.set_expiry(None)
                response['username'] = user_obj.uname

                response['url'] = request.COOKIES.get('url', '/')  # 必须写在ret之前
                ret = JsonResponse(response)
                # print('要回到的url:', request.COOKIES.get('url', '/'))
                # ret.set_cookie('username', user_obj.uname)
                return ret
            else:
                # token验证失败，业务系统可以直接阻断该次请求或者继续弹验证码
                print('登录失败，验证码校验失败')
                response['error_msg'] = '验证码错误'
                response['field'] = 'checkcode'
                return JsonResponse(response)


def logouthandle(request):
    if request.method == 'GET':
        if request.session.get('is_login', None):
            request.session.clear()
        return redirect('/')


def chcode(request):
    if request.method == 'GET':
        stream = BytesIO()
        img, code = create_validate_code()
        img.save(stream, 'PNG')
        # print(type(img), stream.getvalue())
        request.session['register_checkcode'] = code
        return HttpResponse(stream.getvalue())


def findPwd(request):
    if request.POST:
        # print("猪",request.POST.get('captcha_0'), '狗', request.POST.get('captcha_1'))
        findpwd_form = FindPwdForm(request.POST)
        if findpwd_form.is_valid():
            human = True
            print("验证码正确", findpwd_form.cleaned_data)
            # 设置redis缓存
            settings.CONN.hset('email_%s' % (findpwd_form.cleaned_data['femail']), 'newpwd',
                               findpwd_form.cleaned_data['new_passwd'])
            findpwd_form.cleaned_data['status'] = True
            print(findpwd_form.cleaned_data)
            return JsonResponse(findpwd_form.cleaned_data)
        else:
            print('验证码错误', findpwd_form.errors)
            findpwd_form.cleaned_data['status'] = False
            return JsonResponse(findpwd_form.errors)

    elif request.GET:
        # 接收邮件的激活请求
        code_email = request.GET.get('code')
        email_obj = EmailVerify.objects.filter(code=code_email).first()
        if email_obj:
            print('存在该验证请求')
            newpasswd = settings.CONN.hget('email_' + email_obj.email, 'newpwd')
            if newpasswd:
                print("链接有效")
                user_obj = RegUser.objects.filter(uemail=email_obj.email).first()
                user_obj.upasswd = hmac.new(newpasswd).hexdigest()
                user_obj.save()
                print('新密码已暂存于redis数据库中，5分钟后失效')
                del_resetpwd.delay('email_' + email_obj.email)
                print('已celery异步处理key')
                return render(request, 'userapp/index.html', {'res_resetpwd': 'success'})
            else:
                print('验证链接失效')
                return render(request, 'userapp/index.html', {'res_resetpwd': 'invalid'})
        return render(request, 'userapp/index.html')
        # return render(request, 'userapp/index.html', {'res_resetpwd': 'non_exist'})
