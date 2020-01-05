from django.shortcuts import render, redirect
from .ConfigForm import ConfigForm
from topicapp.models import TopicInfo, ChoiceSub, FillbankSub
from userapp.models import RegUser
from django.http import JsonResponse
# from utils.valid_user import outer
from utils.valid_user import auth, auth_organ, auth2
from django.core.exceptions import ValidationError
import json, pickle
from datetime import datetime, date
from .models import MatchConfig, MatchReport
from topicapp.config import DBNOTEXIST_ERROR
from .InfoModelForm import UserExtraInfoForm
from django.urls import reverse
from utils.errors import CompetitionError, UserError
from .InfoModelForm import UserExtraInfoForm
from django.db import transaction
import time
import uuid
import random
import pytz
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Max


# Create your views here.

class JsonExamEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ValidationError):
            print('V')
            return {'code': o.code, 'message': o.message}
        elif isinstance(o, datetime):
            print('DT')
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, date):
            print('D')
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, bytes):
            print('B')
            return str(o, encoding='utf-8')
        # elif isinstance(o, ):
        #     print('B')
        #     return str(o, encoding='utf-8')
        else:
            # 原样输出
            print('原样')
            return json.JSONEncoder.default(self, o)


# @outer('topic', 'do_organ')
@auth
@auth_organ
def set_game(request):
    if request.method == 'GET':
        form_obj = ConfigForm()

        # topicinfo_list = TopicInfo.objects.values('id', 'qname', 'qtype', 'qsize')
        topicinfo_list = TopicInfo.objects.values()  # 不指定字段，全部显示

        current_user = request.session.get('username', None)
        user_obj = RegUser.objects.filter(uname=current_user).first()

        # print(user_obj.authuser.oname)
        return render(request, "matchapp/set_game.html",
                      {'form_obj': form_obj, 'topicinfo_list': topicinfo_list, 'user_obj': user_obj})
    elif request.method == 'POST':
        if request.is_ajax():
            config_form = ConfigForm(request.POST)
            ret = {'status': False, 'error': None, 'data': None, 'obj_id': 0}  # 必须在初始化字典时有obj_id,key否则前端获取不到
            if config_form.is_valid():
                print('验证通过')
                print(config_form.cleaned_data)

                # 保存到数据库
                save_dict = {
                    'mname': config_form.cleaned_data['mname'],
                    'mtime': config_form.cleaned_data['mtime'],
                    'topicount': config_form.cleaned_data['topicount'],
                    # 'score': config_form.cleaned_data['score'],
                    'stime': config_form.cleaned_data['stime'],
                    'etime': config_form.cleaned_data['etime'],
                    'mregular': config_form.cleaned_data['mregular'],
                    'isaddinfo': config_form.cleaned_data['extrainfo'],
                    # 外键字段
                    'qinfo_id': config_form.cleaned_data['qid']['id'],
                    'auinfo_id': config_form.cleaned_data['aid']['id'],
                }
                # 可选字段
                if config_form.cleaned_data['extrainfo']:
                    for field in json.loads(config_form.cleaned_data['otherinfo']):
                        save_dict[field] = 1
                    # 下拉框字段
                    option = ''
                    if 'choicefield' in config_form.cleaned_data:
                        for fielddict in json.loads(config_form.cleaned_data['choicefield']):
                            name = fielddict['name']
                            verbose = fielddict['verbose']
                            value = fielddict['value']
                            suboption = '%s:%s:%s,' % (name, verbose, value)
                            option += suboption
                        save_dict['option_fields'] = option

                try:
                    with transaction.atomic():
                        # 题库部分解析
                        topic_obj = TopicInfo.objects.filter(pk=save_dict['qinfo_id']).first()
                        topic_obj.qhasmatch += 1
                        # 更新题库信息
                        topic_obj.save()

                        match_obj = MatchConfig.objects.create(**save_dict)
                except Exception as e:
                    ret['status'] = False
                else:
                    ret['status'] = True
                    ret['obj_id'] = match_obj.id  # 字典在初始化时，必须写上Key,可能与safe=False有关吧
                    ret['data'] = config_form.cleaned_data
                    print("ret:", ret)
                    ret = json.dumps(ret, cls=JsonExamEncoder)

                return JsonResponse(json.loads(ret), safe=False)
            else:
                print('验证不通过')
                print(config_form.errors)
                # ret['errors'] = config_form.errors.data()
                # TypeError: Object of type '__proxy__' is not JSON serializable

                ret['error'] = json.loads(config_form.errors.as_json())
                ret = json.dumps(ret, cls=JsonExamEncoder)
                return JsonResponse(json.loads(ret), safe=False)
                # In order to allow non-dict objects to be serialized set the safe parameter to False.


def matchinfo(request, mid):
    if request.method == 'GET':
        match_obj = MatchConfig.objects.filter(pk=int(mid)).first()
        if not match_obj:
            return render(request, 'err.html', {'errmsg': CompetitionError.CompetitionRequestError[1] + ' 当前页面已飞向银河系了，要不你去找啊'})
        # 如果页面存在
        code = uuid.uuid4().hex  # 将uuid对象转换成16进制的字符串
        current_url = reverse('match:exam', kwargs=({'mid': mid, 'tokencode': code}))
        response = {'match_obj': match_obj, 'current_url': current_url}

        # 思路:
        # 对于input框字段，可以根据数据库返回的布尔值选择性的显示出来
        # 对于下拉框字段，js优先判断，二者取一
        if not match_obj.isaddinfo:
            return render(request, "matchapp/matchinfo.html", response)

        loop_list = []

        # 先判断普通字段
        extrafields = []
        if match_obj.uname:
            extrafields.append(['true', 'uname', '姓名', 'answeruname'])
        if match_obj.uemail:
            extrafields.append(['true', 'uemail', '邮箱', 'answeruemail'])
            # extrafields.append(match_obj.uemail)
        if match_obj.ugender:
            extrafields.append(['true', 'ugender', '性别', 'answerugender'])
            # extrafields.append(match_obj.ugender)
        if match_obj.uschool:
            extrafields.append(['true', 'uschool', '毕业院校', 'answeruschool'])
            # extrafields.append(match_obj.uschool)
        if match_obj.uweixin:
            extrafields.append(['true', 'uweixin', '微信', 'answeruweixin'])
            # extrafields.append(match_obj.uweixin)
        if match_obj.uage:
            extrafields.append(['true', 'uage', '年龄', 'answeruage'])
            # extrafields.append(match_obj.uage)
        if match_obj.uaddr:
            extrafields.append(['true', 'uaddr', '地址', 'answeruaddr'])
            # extrafields.append(match_obj.uaddr)
        if match_obj.umobile:
            extrafields.append(['true', 'umobile', '手机号', 'answerumobile'])
            # extrafields.append(match_obj.umobile)
        if match_obj.uid:
            extrafields.append(['true', 'uid', '身份证号', 'answeruid'])
            # extrafields.append(match_obj.uid)
        if not extrafields:
            return render(request, 'matchapp/matchinfo.html', response)

        # 再判断下拉框
        if match_obj.option_fields:
            field_list = match_obj.option_fields.split(',')
            # 最后一个,切出一个空列表
            field_list.pop()
            for field in field_list:
                sub_list = []
                partion = field.split(':')
                sub_list.append('true')
                sub_list.append(partion[0])  # Html中的name属性
                sub_list.append(partion[1])  # 中文显示
                sub_list.append('answer' + partion[0])  # 用于自动生成html标签的id
                sub_list.append(partion[2].split('#'))  # 下拉框选项
                loop_list.append(sub_list)

                # 如果普通字段与下拉框字段重复，删除普通字段
                for item in extrafields:
                    if partion[0] == item[1]:
                        extrafields.remove(item)
            for item in extrafields:
                loop_list.append(item)
            response['loop_list'] = loop_list
            return render(request, "matchapp/matchinfo.html", response)

        # 只有普通字段存在的情况
        # loop_list.append(extrafields)
        response['loop_list'] = extrafields
        response['mid'] = int(mid)
        return render(request, "matchapp/matchinfo.html", response)

        # elif request.method == 'POST':
        #     return render(request, "matchapp/matchinfo.html")


# 交卷
# @outer('topic', 'do_organ')
@auth
def matchdetail(request, mid, tokencode):
    current_user = request.session.get('username', None)
    user_obj = RegUser.objects.filter(uname=current_user).first()
    match_obj = MatchConfig.objects.filter(pk=int(mid)).first()
    if (not match_obj) or (not user_obj):
        return render(request, 'err.html',
                      {'errmsg': CompetitionError.CompetitionRequestError[1] + "...检查url是否正确，或者用户的登录状态"})
    exam_dict = {}
    exam_list = []
    if request.method == 'GET':
        ''' 该方法不适用于：页面含有倒计时，记住上一次的用户选择，因为分页每次请求url都是一个新的页面
        handle_type = request.POST.get('bisiness', None)
        # 判断当前的考试环境的url是否有效
        get_url_b = settings.CONN.get('exam:%s:%d' % (mid, user_obj.id))
        if not get_url_b:
            return render(request, 'err.html', {'errmsg': CompetitionError.CompetitionRequestError[1] + "...当前考试已结束。"})
        get_url = get_url_b.decode('utf-8')
        answer_url = reverse('match:exam', kwargs=({'mid': int(mid), 'tokencode': get_url}))
        # 获取原先的题目列表
        exam_list_b = settings.CONN.zrange('exam:%s:%d:detail:exam_list' % (mid, user_obj.id), 0, -1)
        for item in exam_list_b:
            exam_list.append(pickle.loads(item))
        stime = (settings.CONN.hmget('exam:%s:%d:detail:answer_dict' % (mid, user_obj.id), 'stime'))[0].decode('utf-8')
        print('stime', stime)
        timed = (time.time() - float(stime))/60

        print(handle_type, exam_list, answer_url, exam_list[0].id)
        page_obj = Paginator(exam_list, 1)
        objs = page_obj.page(int(request.GET.get('pindex', 1)))
        plist = page_obj.page_range
        exam_dict['objs'] = objs
        exam_dict['plist'] = plist
        # exam_dict['answer_url'] = answer_url
        print(exam_dict)

        exam_dict['match_info'] = match_obj
        exam_dict['mtime'] = match_obj.mtime - int(timed)
        return render(request, 'matchapp/matchdetail.html', exam_dict)
        '''

        # 禁止用户get请求进入考试系统
        return render(request, 'err.html',
                      {'errmsg': CompetitionError.CompetitionRequestError[1] + "...您已退出考试系统，无法继续考试"})
    elif request.method == 'POST':
        # 因为该post请求需要接收4钟类型的逻辑处理
        # 所以需要分开：(1)进入答题环境、(2)上一页、(3)下一页、(4)交卷，1使用的submit提交，2,3,4使用ajax提交，并且使用redis保存临时数据
        if not request.is_ajax():
            # 先判断比赛配置是否过期
            # print("数据库中获取的时间是datetime类型，且是UTC时间", match_obj.etime)
            if datetime.now(pytz.utc) > match_obj.etime:
                return render(request, 'err.html', {'errmsg': UserError.UserNotFound[1] + ' 该比赛已结束'})

            # (1)本模块中进入环境没有用ajax提交数据
            # post进入下面的页面后，再js刷新页面会继承上次的请求方式get/post
            if not current_user:
                return render(request, 'err.html', {'errmsg': UserError.UserNotFound[1]})

            # OnetoOne关系，反查时，主表必须有对应的数据，否则，它不能使用.related_name字段进行跨表
            # 还有：OnetoOne反查不能通过表名_set反查，只能通过related_name反查
            if request.session.get('is_auth'):  # 是机构用户
                if match_obj.auinfo_id == user_obj.authuser.id:
                    return render(request, 'err.html', {'errmsg': CompetitionError.CompetitionObjectError[1]})

            # 正常接收数据的业务逻辑
            # 仅需一个简单的后端验证即可
            extramodel_form = UserExtraInfoForm(request.POST)
            if extramodel_form.is_valid():
                print('验证通过')
                # print(extramodel_form.cleaned_data)

                with transaction.atomic():
                    # 对数据进行过滤后，再保存到数据库
                    field_dict = {}
                    for field, value in extramodel_form.cleaned_data.items():
                        if not value:
                            continue
                        field_dict[field] = value
                    # userprofile_obj = UserProfile.objects.create(**field_dict)
                    # 最后统一创建数据库,即交卷时才创建，超时、未完成都不创建数据库

                    answer_dict = {
                        'status': 1,
                        'stime': time.time(),
                        'usedtime': 0,
                        'resgrade': 0,
                        # 'userinfo_id': userprofile_obj.id,
                        'baseuser_id': user_obj.id,
                        'curmatch_id': int(mid),
                    }
                    # MatchReport.objects.create(**answer_dict)
                    # 最后统一创建数据库,即交卷时才创建，超时、未完成都不创建数据库

                    # 设置url后缀tokencode的有效期,避免get请求直接访问
                    # 设置tokencode的有效期为考试的总时间
                    totaltime = match_obj.mtime
                    time_out = int((totaltime + 0.1 / 6) * 60)
                    settings.CONN.setex('exam:%s:%d' % (mid, user_obj.id), time_out, tokencode)

                    # 保存上面的两个字典到redis缓存中
                    if field_dict:
                        settings.CONN.hmset('exam:%s:%d:detail:field_dict' % (mid, user_obj.id), field_dict)
                    settings.CONN.hmset('exam:%s:%d:detail:answer_dict' % (mid, user_obj.id), answer_dict)
                    # 设置超时时间
                    settings.CONN.expire('exam:%s:%d:detail:field_dict' % (mid, user_obj.id), time_out)
                    settings.CONN.expire('exam:%s:%d:detail:answer_dict' % (mid, user_obj.id), time_out)

                    code = settings.CONN.get('exam:%s:%d' % (mid, user_obj.id))
                    if not code:
                        return render(request, 'err.html', {'errmsg': CompetitionError.CompetitionTIMEOUT[1]})
                    answer_url = reverse('match:exam', kwargs=({'mid': int(mid), 'tokencode': code}))

                # 强制用户post请求进入考试系统
                current_topic_obj = TopicInfo.objects.filter(pk=match_obj.qinfo_id).first()
                all_fb_list = list(current_topic_obj.fbinfo.all())  # 所有填空题列表
                all_ch_list = list(current_topic_obj.chinfo.all())  # 所有选择题列表

                # 分别获取填空题、选择题数量
                fb_len = len(all_fb_list)
                ch_len = len(all_ch_list)
                # 获取这场比赛的题库大小
                size = current_topic_obj.qsize
                # 获取这场比赛的总题数
                count = match_obj.topicount

                if count < size:
                    # 从选择题中随机获取数目（包括全部和没有）
                    random_fb_count = random.randint(0, fb_len)
                    random_ch_count = count - random_fb_count

                    # 先打乱列表顺序，再获取前几个
                    random.shuffle(all_fb_list)
                    random.shuffle(all_ch_list)
                    for i in range(random_fb_count):  # 仅用于控制循环的次数
                        exam_list.append(all_fb_list[i])
                    for i in range(random_ch_count):
                        exam_list.append(all_ch_list[i])
                else:
                    exam_list = all_fb_list + all_ch_list
                random.shuffle(exam_list)

                exam_dict['exam_list'] = exam_list
                exam_dict['match_info'] = match_obj
                exam_dict['answer_url'] = answer_url

                # 分页,如果页面显示数量就1条，可以使用js隐藏和显示来达到分页效果
                ''' 分页走不通了
                page_obj = Paginator(exam_list, 1)
                objs = page_obj.page(1)
                plist = page_obj.page_range
                exam_dict['objs'] = objs
                exam_dict['plist'] = plist

                # 保存已打乱顺序的对象列表到redis缓存中, model类对象可以使用pickle.dumps进行序列化，json不能
                i = 0
                for obj in exam_list:
                    settings.CONN.zadd('exam:%s:%d:detail:exam_list' % (mid, user_obj.id), {pickle.dumps(obj): i})
                    i += 1
                '''

                return render(request, 'matchapp/matchdetail.html', exam_dict)
                # return redirect(answer_url)
            else:
                print('验证不通过')
                load_url = reverse('match:info', kwargs={'mid': int(mid)})
                return redirect(load_url)

        else:  # 使用ajax提交的业务逻辑处理(交卷)
            # 判断当前的考试环境的url是否有效
            get_url_b = settings.CONN.get('exam:%s:%d' % (mid, user_obj.id))
            if not get_url_b:
                return render(request, 'err.html',
                              {'errmsg': CompetitionError.CompetitionRequestError[1] + "...当前考试已结束。"})

            question_record = []
            answer_record = []
            right_list = []
            error_list = []
            right_count = 0
            error_count = 0
            data_list = json.loads(request.POST.get('exam'))
            question_count = len(data_list)
            is_finish = 0
            score = 0
            # 解析列表嵌套字典
            for item_dict in data_list:
                question_record.append(item_dict['title'])
                answer_record.append(item_dict['answer'])
                if item_dict['type'] == 'ch':
                    # 找答案
                    obj = ChoiceSub.objects.filter(title=item_dict['title']).first()
                else:
                    obj = FillbankSub.objects.filter(title=item_dict['title']).first()

                # 判断obj对象是否存在，NoneType没有任何属性
                print("obj:", obj)
                if not obj:
                    return JsonResponse({'error': '题库故障'})

                if obj.answer == item_dict['answer']:
                    right_list.append(item_dict['title'])
                    right_count += 1
                    score += obj.perSore
                else:
                    if item_dict['answer'] == '':
                        is_finish = 1
                        # print('本题漏答')
                    error_list.append(item_dict['title'] + ' 您的答案：' + item_dict['answer'] + '标准答案' + obj.answer)
                    error_count += 1

            # 从redis中获取和更新考试前的用户的数据表
            field_dict = settings.CONN.hgetall('exam:%s:%d:detail:field_dict' % (mid, user_obj.id))
            answer_dict = settings.CONN.hgetall('exam:%s:%d:detail:answer_dict' % (mid, user_obj.id))

            # 用户字段
            if field_dict:
                # userprofile_obj = UserProfile.objects.create(**field_dict)
                RegUser.objects.filter(pk=user_obj.id).update(**field_dict)
                # create/update之后返回的不是对象，而是int类型的数据库id

            # 获取当前时间
            format_time = "%Y-%m-%d %H:%M:%S"
            etimes = time.time()
            stimes = float(answer_dict['stime'])
            usedtime = round(etimes - stimes, 1)

            # 转换交卷时间
            etime = time.strftime(format_time)
            # 转换答题开始时间
            # 先把时间戳转成元组
            tup = time.localtime(stimes)
            # 再把元组转成格式化字符串
            stime = time.strftime(format_time, tup)

            # 外键
            match_id = match_obj.id

            answer_dict = {
                'status': is_finish,
                'question_record': question_record,
                'answer_record': answer_record,
                'stime': stime,
                'etime': etime,
                'right_list': right_list,
                'error_list': json.dumps(error_list),
                'right_count': right_count,
                'error_count': error_count,
                'question_count': question_count,
                'usedtime': usedtime,
                'resgrade': score,
                # 历史排名不在交卷时写入数据库，而是在展示页面的时候，获取排名和更新数据库
                # 'userinfo_id': user_id,
                'baseuser_id': user_obj.id,
                'curmatch_id': match_id,
            }
            MatchReport.objects.create(**answer_dict)

            # 更新题库的参与人次
            topic_obj = TopicInfo.objects.filter(pk=match_obj.qinfo_id).first()
            topic_obj.qucount += 1
            topic_obj.save()

            return JsonResponse(data_list, safe=False)


def matchrank(request, mid):
    response = {}
    # 在6号比赛中反查所有人的结果报告,并且每个人不重复
    match_obj = MatchConfig.objects.filter(id=int(mid)).first()
    if not match_obj:
        return render(request, 'err.html', {'errmsg': CompetitionError.CompetitionRequestError[1] + ' 没有这样的比赛，或已过期'})
    report_list = MatchReport.objects.filter(curmatch_id=int(mid)).values_list('baseuser_id').annotate(Max('id'))
    id_list = []
    for uid, mrid in list(report_list):
        id_list.append(mrid)
    reports = match_obj.matchreport_set.filter(id__in=id_list).order_by('-resgrade')

    response['reports'] = reports
    response['match_obj'] = match_obj

    # 判断自己在该题库排行榜下是否有答题记录
    username = request.session.get('username', None)
    user_obj = RegUser.objects.filter(uname=username).first()

    if not user_obj:
        return render(request, "matchapp/matchrank.html", response)

    # 我的历史排名
    current_report_obj = MatchReport.objects.filter(baseuser_id=user_obj.id, curmatch_id=int(mid)).first()
    if current_report_obj:
        if not current_report_obj.his_rank:
            cur_report_list = []
        else:
            cur_report_list = json.loads(current_report_obj.his_rank)
        for index, obj in enumerate(list(reports)):
            if obj.baseuser_id == user_obj.id:
                print("#", cur_report_list)
                cur_report_list.append([index + 1, obj.usedtime])
                print("#", cur_report_list)
                cur_report_list.sort()
                if len(cur_report_list) > 5:
                    cur_report_list.pop()

        # 更新数据库
        current_report_obj.his_rank = json.dumps(cur_report_list)
        current_report_obj.save()
    else:
        cur_report_list = []

    response['cur_report_list'] = cur_report_list
    return render(request, "matchapp/matchrank.html", response)


def exam_start(request, mid):
    match_obj = MatchConfig.objects.filter(pk=int(mid)).first()
    if not match_obj:
        return 'error'
    code = uuid.uuid4().hex
    current_url = reverse('match:exam', kwargs=({'mid': mid, 'tokencode': code}))
    response = {'match_obj': match_obj, 'current_url': current_url}

    if not match_obj.isaddinfo:
        return response

    loop_list = []

    extrafields = []
    if match_obj.uname:
        extrafields.append(['true', 'uname', '姓名', 'answeruname'])
    if match_obj.uemail:
        extrafields.append(['true', 'uemail', '邮箱', 'answeruemail'])
    if match_obj.ugender:
        extrafields.append(['true', 'ugender', '性别', 'answerugender'])
    if match_obj.uschool:
        extrafields.append(['true', 'uschool', '毕业院校', 'answeruschool'])
    if match_obj.uweixin:
        extrafields.append(['true', 'uweixin', '微信', 'answeruweixin'])
    if match_obj.uage:
        extrafields.append(['true', 'uage', '年龄', 'answeruage'])
    if match_obj.uaddr:
        extrafields.append(['true', 'uaddr', '地址', 'answeruaddr'])
    if match_obj.umobile:
        extrafields.append(['true', 'umobile', '手机号', 'answerumobile'])
    if match_obj.uid:
        extrafields.append(['true', 'uid', '身份证号', 'answeruid'])
    if not extrafields:
        return response

    if match_obj.option_fields:
        field_list = match_obj.option_fields.split(',')
        field_list.pop()
        for field in field_list:
            sub_list = []
            partion = field.split(':')
            sub_list.append('true')
            sub_list.append(partion[0])  # Html中的name属性
            sub_list.append(partion[1])  # 中文显示
            sub_list.append('answer' + partion[0])  # 用于自动生成html标签的id
            sub_list.append(partion[2].split('#'))  # 下拉框选项
            loop_list.append(sub_list)

            for item in extrafields:
                if partion[0] == item[1]:
                    extrafields.remove(item)
        for item in extrafields:
            loop_list.append(item)
        response['loop_list'] = loop_list
        return response

    response['loop_list'] = extrafields
    response['mid'] = int(mid)
    return response


def checkrank(mid, uid):
    # from django.db.models import Max 已导入
    # 一个人很多成绩，而报告又有很多人的成绩，需要将每个人进行分组统计，找出每个人最大的成绩进行排名

    # report = MatchReport.objects.values_list('baseuser_id').aggregate(Max('id'))
    # print("{'id__max': 13}", report, "只找出baseuser最大的id")

    report_list = MatchReport.objects.filter(curmatch_id=int(mid)).values_list('baseuser_id').annotate(Max('id'))
    # print("<QuerySet [(4, 8), (5, 4), (6, 6), (7, 13), (9, 7)]>", report_list, "分组，并找出所有baseuser最大的id")

    # 拆分列表，取出第二个元素
    mid_list = []
    # 避免u_id与参数uid重名，
    for u_id, m_id in list(report_list):
        mid_list.append(m_id)
    report_obj_list = MatchReport.objects.filter(id__in=mid_list).order_by('-resgrade')
    for index, obj in enumerate(list(report_obj_list)):
        if obj.baseuser_id == uid:
            return index + 1, obj
    return 0, None


# @outer('topic', 'do_organ')
@auth
def matchresult(request, mid):
    username = request.session.get('username', None)
    user_obj = RegUser.objects.filter(uname=username).first()

    res = exam_start(request, mid)

    if res == 'error':
        return render(request, 'err.html', {'errmsg': CompetitionError.CompetitionRequestError[1]})
    if not user_obj:
        return render(request, 'err.html', {'errmsg': "请先登录"})

    rank, self_result_obj = checkrank(mid, user_obj.id)
    if rank:
        res['rank'] = rank
        res['self_result_obj'] = self_result_obj

        # 获取错题的标准答案
        error_list = []
        for error_item in json.loads(self_result_obj.error_list):
            error_title, right_answer = error_item.split('标准答案')
            error_list.append((error_title, right_answer))

        # res['error_list'] = json.loads(self_result_obj.error_list)
        res['error_list'] = error_list
    # print(res)
    return render(request, "matchapp/matchresult.html", res)


def matchlist(request):
    if request.method == 'GET':
        # 只能取指定的这些固定字段，不能再通过.跨表取字段
        queryset_list = MatchConfig.objects.values('id', 'mname', 'etime', 'stime', 'qinfo__qucount', 'auinfo__oname',
                                                   'auinfo_id')

        # 分页：
        paginator_obj = Paginator(queryset_list, 6)
        match_list = paginator_obj.page(int(request.GET.get('pindex', '1')))
        pagenum_list = paginator_obj.page_range

        match_dict = {
            'match_list': match_list,
            'page_list': pagenum_list,
        }
        return render(request, "matchapp/matchlist.html", match_dict)


# @outer('topic', 'do_organ')
@auth2
def matchlist_del(request, mid):
    response = {}
    if request.method == 'GET':
        username = request.session.get('username', None)
        user_obj = RegUser.objects.filter(uname=username).first()
        if not user_obj:
            response['error_del'] = '您没有权限删除该比赛信息'
            return JsonResponse(response)

        # 判断该用户关联的表是否有记录,否则，user_obj.表名报错
        if not request.session.get('is_auth'):
            response['error_del'] = '您没有权限删除该比赛信息'
            return JsonResponse(response)

        authuser_id = user_obj.authuser.id

        match_obj = MatchConfig.objects.filter(pk=int(mid)).first()
        if not match_obj:
            response['error_del'] = '该配置不存在，或已删除'
            return JsonResponse(response)
        if authuser_id != match_obj.auinfo_id:
            print('出错了')
            response['error_del'] = '您没有权限删除此比赛配置'
            return JsonResponse(response)

        # 删除的业务逻辑处理
        match_obj.delete()
        response['success_del'] = '删除成功'
        return JsonResponse(response)


def match_list(request, qid):
    if request.method == 'GET':
        queryset_list = MatchConfig.objects.values('id', 'mname', 'etime', 'stime', 'qinfo__qucount', 'auinfo__oname',
                                                   'auinfo_id', 'qinfo__qtype').filter(qinfo__qtype=int(qid))

        # 已经获得所有的比赛配置信息, 从中筛选和排序即可
        if not queryset_list:
            return render(request, "matchapp/match_list.html", {'match_list': queryset_list})

        # 分页：
        paginator_obj = Paginator(queryset_list, 6)
        match_list = paginator_obj.page(int(request.GET.get('pindex', '1')))
        pagenum_list = paginator_obj.page_range

        match_dict = {
            'match_list': match_list,
            'page_list': pagenum_list,
        }
        return render(request, "matchapp/match_list.html", match_dict)
