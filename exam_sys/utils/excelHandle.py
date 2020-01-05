import xlrd
from topicapp.models import FillbankSub, ChoiceType, FillBankType, ChoiceSub
from django.db import transaction
import traceback
from topicapp.config import choicerror, fillbankerror, topicerror, qsizetoobig


def whattype(rowvalues, tid, ttype):
    if ttype == 'fillbank':
        sub_obj = FillBankType()
    else:
        sub_obj = ChoiceType()
    if rowvalues[6] and rowvalues[7]:  # 图片url/音频url
        sub_obj.cur_type = 3
    elif rowvalues[6]:
        sub_obj.cur_type = 1
    elif rowvalues[7]:
        sub_obj.cur_type = 2
    else:
        sub_obj.cur_type = 0

    # 保存题目类型, manytomany需要先创建对象,才能对三张表操作
    sub_obj.save()

    sub_obj.sub.add(tid)


@transaction.atomic  # 需要将MySQL数据库隔离级别设置为RC
def temp_handle(filename):
    '''
    模板文件的解析函数,以及excel知识点的应用
    :param filename: 用户上传的题库模板文件名
    :return: 填空题、选择题数量
    '''
    # 初始变量计数值
    repeat_fillbank = 0
    repeat_choice = 0
    fillbank_num = 0
    choice_num = 0
    fillbank_list = []
    choice_list = []

    # 读取文件
    book = xlrd.open_workbook(filename)
    # 获取第一张表
    table = book.sheets()[0]
    # 获取行数
    nrows = table.nrows
    if nrows > 50:
        return qsizetoobig()

    # 这里设置乐观锁仅尝试1次保存
    s1 = transaction.savepoint()

    # 从第二行开始循环所有的行
    for line in range(1, nrows):
        # 获取每一行的数据
        rowvalues = table.row_values(line)

        # 如果第一行是空行或以“说明”开头就退出解析，不执行下面代码
        if (not rowvalues[0]) or rowvalues[0].startswith('说明'):
            break

        # print("下面将开始题型判断...")
        try:
            # ##表示填空题
            if "##" in rowvalues[0]:
                # 先判断题目标题是否重复
                fillbank_obj = FillbankSub.objects.filter(title=rowvalues[0]).first()
                if fillbank_obj:
                    repeat_fillbank += 1
                    # print('填空题目重复%d题' % repeat_fillbank)

                    # 虽然题目重复，但是它是属于该题库的
                    fillbank_list.append(fillbank_obj.id)
                    continue

                try:
                    fillbank_obj = FillbankSub()
                    fillbank_obj.title = rowvalues[0]
                    fillbank_obj.answer = rowvalues[1]
                    fillbank_obj.image_url = rowvalues[6]
                    fillbank_obj.audio_url = rowvalues[7]
                    fillbank_obj.source = rowvalues[8]

                    fillbank_obj.perSore = rowvalues[9]

                except IndexError as e:
                    # print('填空题列数设置有误')
                    # raise ValidationError('第%d行填空题格式设置有误' % line, code=FILLBANKCOL_ERROR)
                    return fillbankerror(line)
                else:
                    # 保存题目
                    fillbank_obj.save()
                    fillbank_num += 1

                    whattype(rowvalues, fillbank_obj.id, 'fillbank')

                    # 关联到题库
                    fillbank_list.append(fillbank_obj.id)
            else:
                # 先判断选择题标题有无重复
                choice_obj = ChoiceSub.objects.filter(title=rowvalues[0]).first()
                if choice_obj:
                    repeat_choice += 1
                    # print("选择题重复%d题" % repeat_choice)

                    # 虽然题目重复，但是它是属于该题库的
                    choice_list.append(choice_obj.id)
                    continue
                try:
                    choice_obj = ChoiceSub()
                    choice_obj.title = rowvalues[0]
                    choice_obj.answer = rowvalues[1]

                    choice_obj.radio1 = rowvalues[2]
                    choice_obj.radio2 = rowvalues[3]
                    choice_obj.radio3 = rowvalues[4]
                    choice_obj.radio4 = rowvalues[5]

                    choice_obj.image_url = rowvalues[6]
                    choice_obj.audio_url = rowvalues[7]
                    choice_obj.source = rowvalues[8]

                    choice_obj.perSore = rowvalues[9]

                except IndexError as e:
                    # print('选择题列数设置有误')
                    # raise ValidationError('第%d行格式错误' % line, code=CHOICECOL_ERROR)
                    return choicerror(line)
                else:
                    # 保存题目
                    choice_obj.save()
                    choice_num += 1

                    # 异常处理判断
                    # choice_obj.source = rowvalues[9]
                    whattype(rowvalues, choice_obj.id, 'choice')

                    # 关联到题库
                    choice_list.append(choice_obj.id)
        except Exception as e:
            transaction.savepoint_rollback(s1)
            traceback.print_exc()
            # raise ValidationError('题库解析出错了', code=TOPICPARSE_ERROR)
            return topicerror()

    transaction.savepoint_commit(s1)
    # transaction.savepoint_rollback(s1)
    # print('所有题目解析成功，已保存到数据库')

    backdata_dict = {
        'qsize': fillbank_num + choice_num + repeat_choice + repeat_fillbank,
        'qfillblank': fillbank_num + repeat_fillbank,
        'qselect': choice_num + repeat_choice,
        'repeat_fillbank': repeat_fillbank,
        'repeat_choice': repeat_choice,
    }
    if fillbank_list:
        backdata_dict['fbinfo'] = fillbank_list
    if choice_list:
        backdata_dict['chinfo'] = choice_list
    return backdata_dict
