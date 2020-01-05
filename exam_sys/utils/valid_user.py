# from userapp.models import RegUser, AuthUser
import functools
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse


'''
def outer(app, url_app):
    def auth(func):
        @functools.wraps(func)
        def wrap(request, *args, **kwargs):
            islogin = request.session.get('is_login', None)
            if not islogin:
                # cur_path = request.path_info + '?do=login' # 不可以这样做,死循环重定向
                cur_path = reverse(app+":"+url_app) + '?do=login'
                return redirect(cur_path)
            # 如果用户已登录,登录处理视图中已经设置了是否是机构用户的session值
            return func(request, *args, **kwargs)

        return wrap
    return auth
'''


def auth(func):
    @functools.wraps(func)
    def wrap(request, *args, **kwargs):
        islogin = request.session.get('is_login', None)
        if not islogin:
            cur_path = reverse("topic:do_organ") + '?do=login'  # 可以这样做
            ret = redirect(cur_path)
            ret.set_cookie('url', request.get_full_path())
            # print("当前url:", request.get_full_path())
            return ret
        # 如果用户已登录,登录处理视图中已经设置了是否是机构用户的session值, 暂时不考虑该问题
        return func(request, *args, **kwargs)

    return wrap


def auth_organ(func):
    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        is_auth = request.session.get('is_auth', 0)
        if not is_auth:
            cur_path = reverse("topic:do_organ")
            ret = redirect(cur_path)
            ret.set_cookie('url', request.get_full_path())
            return ret
        return func(request, *args, **kwargs)
    return inner


def auth2(func):
    @functools.wraps(func)
    def wrap(request, *args, **kwargs):
        islogin = request.session.get('is_login', None)
        if not islogin:
            return JsonResponse({'error_del': '你需要登录哦~'})
        return func(request, *args, **kwargs)

    return wrap
