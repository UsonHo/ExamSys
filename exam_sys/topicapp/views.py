from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from topicapp.organform import OrganModelForm
from userapp.models import AuthUser, RegUser
# from utils.valid_user import outer
from utils.valid_user import auth, auth_organ

# 上传题库
from .uploadTopicModelform import UploadTopicModelForm
from .models import TopicInfo


# Create your views here.

def do_organ(request):
    if request.method == 'POST':
        cur_user = request.session.get('username', None)
        # print('当前用户：', cur_user)
        if cur_user:
            cur_user_obj = RegUser.objects.filter(uname=cur_user).first()
            cur_user_id = cur_user_obj.id
        else:
            cur_user_id = None
        # print("shuju", request.POST.get('userinfo', None))  # 7
        up_organ_obj = OrganModelForm(request.POST, login_user=cur_user_id)
        if up_organ_obj.is_valid():
            print("验证通过")
            human = True
            up_organ_obj.cleaned_data['status'] = 1

            # 设不设置无所谓
            # up_organ_obj.cleaned_data['userinfo_id'] = up_organ_obj.cleaned_data['userinfo'].id
            # up_organ_obj.cleaned_data['userinfo_id'] = cur_user_id

            # print('类型', up_organ_obj.cleaned_data)
            # 类型 {'status': 1, 'oemail': 'cohui@cohui.top', 'oname': '上海尚孔教育有限公司', 'oreluname': 'uson',
            # 'oumobile': '17334*****', 'otype': '4', 'userinfo': <RegUser: RegUser object (7)>}
            # 虽然在验证前获取到的是用户userinfo_id=7，但是在验证后，就是一个对象<RegUser: RegUser object (7)>,需要序列化才能传入前端
            # 并且已把userinfo_id=7通过save()保存到了数据库

            # print(up_organ_obj.cleaned_data['userinfo'].id)
            # auth_user_obj = AuthUser.objects.create(**up_organ_obj.cleaned_data)
            up_organ_obj.save()
            request.session['is_auth'] = True

            user_obj = RegUser.objects.filter(id=cur_user_id).first()
            user_obj.isauth = 1
            user_obj.save()

            from django.core import serializers
            up_organ_obj.cleaned_data['userinfo'] = serializers.serialize('json', queryset=RegUser.objects.filter(
                id=cur_user_id))

            return JsonResponse(up_organ_obj.cleaned_data, content_type='application/json')
        else:
            print("验证不通过")
            return JsonResponse(up_organ_obj.errors)
    elif request.method == 'GET':
        if not request.is_ajax():
            aobj = OrganModelForm()
            user_obj = RegUser.objects.filter(uname=request.session.get('username', None)).first()
            return render(request, 'topicapp/do_organ.html', {'otypes': aobj, 'user_obj': user_obj})

        response = {'status': False}
        ophone = request.GET.get('oumobile')
        print("手机号:", ophone)
        from utils.yuntongxun.SendTemplateSMS import ccp
        from utils.yuntongxun import config
        code = ccp.generatecode(ophone)
        res = ccp.sendTemplateSMS(ophone, [code, config.EXPIREMIN], config.TEMPID)
        response['status'] = res
        return JsonResponse(response)


'''
def set_question_login(request):
    return render(request, 'topicapp/err.html')
'''


# @outer('topic', 'do_organ')
@auth
def set_question(request):
    return render(request, "topicapp/set_requestion.html")


# @outer('topic', 'do_organ')
@auth
@auth_organ
def set_question_set(request):
    '''
    上传题库
    :param request: 用户请求
    :return: 验证失败，返回errors提示信息；验证成功，展示题库信息
    '''
    if request.method == 'POST':
        topic_modelform = UploadTopicModelForm(request.POST, request.FILES)
        if topic_modelform.is_valid():
            print('验证通过')

            # 解析文件到数据库
            # print("是个什么东西, 一堆html代码", topic_modelform)

            # print(topic_modelform.cleaned_data)

            topicinfo_obj = TopicInfo.objects.create(
                qtype=topic_modelform.cleaned_data['qtype'],
                qname=topic_modelform.cleaned_data['qname'],
                qsize=topic_modelform.cleaned_data['qsize'],
                qselect=topic_modelform.cleaned_data['qselect'],
                qfillblank=topic_modelform.cleaned_data['qfillblank'],
                aid=topic_modelform.cleaned_data['aid']
            )
            if 'fbinfo' in topic_modelform.cleaned_data:
                topicinfo_obj.fbinfo.add(*topic_modelform.cleaned_data['fbinfo'])
            if 'chinfo' in topic_modelform.cleaned_data:
                topicinfo_obj.chinfo.add(*topic_modelform.cleaned_data['chinfo'])

            # 把不需要传给前端的数据删除，就不用单独序列化
            topic_modelform.cleaned_data.pop('qfile')
            topic_modelform.cleaned_data.pop('aid')

            topic_modelform.cleaned_data['status'] = True

            return JsonResponse(topic_modelform.cleaned_data)
            # return render(request, 'topicapp/set_question_set.html')
        else:
            print('验证不通过')
            # print(topic_modelform.errors)
            # print(topic_modelform.errors['qfile'][0])
            '''
            topic_modelform.errors.as_json():
             {key: [json_key: 字符串]} topic_modelform.errors.as_json()['qfile'][0]  取值需要json.loads()
            {"qfile": [{"message": "\u9898\u5e93\u540d\u5df2\u5b58\u5728\uff0c\u8bf7\u91cd\u65b0\u4fee\u6539\u540e\u63d0\u4ea4", "code": 1002}]}

            topic_modelform.errors:
            <ul class="errorlist"><li>qfile<ul class="errorlist"><li>题库名已存在，请重新修改后提交</li></ul></li></ul>
            '''

            import json
            error = json.loads(topic_modelform.errors.as_json())
            return JsonResponse(error)

    elif request.method == 'GET':
        uploadtopic_mf = UploadTopicModelForm()
        user_obj = RegUser.objects.filter(uname=request.session['username']).values_list('authuser__id').first()
        return render(request, "topicapp/set_question_set.html", {'uploadtopic_mf': uploadtopic_mf, 'user_obj': user_obj})


# @outer('topic', 'do_organ')
@auth
@auth_organ
def download_template(request):
    if request.method == "GET":
        from django.conf import settings
        from utils.errors import TemplateNotFound
        import os
        temp_path = os.path.join(settings.MEDIA_ROOT, 'templatefile/template.xlsx')
        if not os.path.exists(temp_path):
            return render(request, 'err.html', TemplateNotFound)

        def iterator(filename, chunk_size=512):
            with open(temp_path, 'rb') as fr:
                while True:
                    recvdata = fr.read(chunk_size)
                    if not recvdata:
                        break
                    else:
                        yield recvdata

        response = HttpResponse(iterator(temp_path), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=template.xlsx'  # 修改格式为xlsx
        return response
