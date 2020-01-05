/**
 * Created by uson on 19-12-24.
 */

$(function () {
    var tid = 7;
    var topicButton = $('.mysetquestion .leftSet .topictype');
    var ulMenu = $('.mysetquestion .leftSet .dropdown .dropdown-menu');
    ulMenu.delegate('li', 'click', function () {
        var selectedType = $(this).text();
        topicButton.val(selectedType);

        tid = $(this).children(":first").val();
        topicButton.attr('tid', tid);

        fixShow(tid);
        /*
         // 每次点击题库类型时，自动筛选出对应的所有题库名,后端一次性展示，前端控制显示
         tid = $(this).children(":first").val();
         var kuLi = $('.mysetquestion .leftSet .selectKu li');
         var eqtid = $('li[type=' + tid + ']');
         kuLi.not(eqtid).each(function (k) {
         $(this).hide();
         });

         // 如果超过显示条数10，就会收到下拉框中
         kuLi.filter(eqtid).each(function (k) {
         if (k < 10) {
         $(this).show();
         }else if(k == 10){
         $('.mysetquestion .leftSet .dropup').removeClass('hide');
         $('.mysetquestion .leftSet .dropup ul').append($(this).show());
         }else if(k > 10){
         $('.mysetquestion .leftSet .dropup ul').append($(this).show());
         }
         });
         */
    });
    fixShow(tid);
    function fixShow(tid) {
        // 每次点击题库类型时，自动筛选出对应的所有题库名,后端一次性展示，前端控制显示
        $('.mysetquestion .leftSet .dropup').addClass('hide');
        var kuLi = $('.mysetquestion .leftSet .selectKu li');
        var eqtid = $('li[type=' + tid + ']');
        kuLi.not(eqtid).each(function (k) {
            $(this).hide();
        });

        // 如果超过显示条数10，就会收到下拉框中
        kuLi.filter(eqtid).each(function (k) {
            if (k < 10) {
                $(this).show();
            } else if (k == 10) {
                $('.mysetquestion .leftSet .dropup').removeClass('hide');
                $('.mysetquestion .leftSet .dropup ul').append($(this).show());
            } else if (k > 10) {
                $('.mysetquestion .leftSet .dropup ul').append($(this).show());
            }
        });
    }

    // 更多题库
    function dynamicWidth() {
        var leftMoreWidth = $('.container .row').width() - 32;
        $('.mysetquestion .selectKu .dropup .dropdown-menu').width(leftMoreWidth + 'px');
    }

    dynamicWidth();
    $(window).resize(function (e) {
        dynamicWidth();
        matchWordsLimit();
    });

    $('.mysetquestion #myModal .midinfo .modal-footer :button').click(function () {
        $('.mysetquestion .modal').hide();
        $('#myModal .mask, .mysetquestion #myModal .midinfo').addClass('hide');
    });

    // 选择题库
    var num;
    $('.mysetquestion .selectKu li').click(function (k) {
        // 自定义属性，用来获取上次的点击标签,根据该属性以及下次动作做出相应的行为
        $(this).attr('clicked', 'clicked').siblings().removeAttr('clicked');

        // 点击题库，弹出题库信息详细内容
        $('.mysetquestion .modal').show();
        $('#myModal .leftinfo, #myModal .mask').removeClass('hide');

        // 获取题库详细信息
        var value_list = $(this).next().text().split(':');
        $('.leftinfo .modal-body .qname').text(value_list[0]);
        $('.leftinfo .modal-body .qtype').text(value_list[1]);
        $('.leftinfo .modal-body .qsize').text(value_list[2]);
        $('.leftinfo .modal-body .qselect').text(value_list[3]);
        $('.leftinfo .modal-body .qfillblank').text(value_list[4]);
        $('.leftinfo .modal-body .qucount').text(value_list[5]);
        $('.leftinfo .modal-body .qhasmatch').text(value_list[6]);

        // 获取出题数量,用于点击使用题库后更新数据
        var selectLi = $(this).text();
        var rep = /共(\d+)题/;
        num = rep.exec(selectLi)[1];
        // input_subcount.val(num);
    });
    // 当点击了使用题库后，自动更新默认出题数量
    $('.leftinfo .modal-footer button').click(function (k) {
        input_subcount.val(num);

        $('.mysetquestion .selectKu li').filter('li[clicked="clicked"]').addClass('def_active').siblings().removeClass('def_active');

        $('.mysetquestion .modal').hide();
        $('#myModal .leftinfo, #myModal .mask').addClass('hide');
    });

    // 配置比赛表单的验证信息(中间部分)
    var matchName = false;
    var orgaName = false;
    var score = false;
    var subCount = false;
    var setTime = false;
    var usetTime = false;
    var examTime = false;
    var midForm = $('.mysetquestion .midSet #matchConfig input');
    var input_matchname = midForm.filter('input[name="matchname"]');   // 是从选中的标签中过滤，而不是在其子标签中过滤提取
    var input_organame = midForm.filter('input[name="organame"]');
    var input_score = midForm.filter('input[name="score"]');
    var input_subcount = midForm.filter('input[name="subcount"]');
    var input_settime = midForm.filter('input[name="settime"]');
    var input_usettime = midForm.filter('input[name="usettime"]');
    var input_examtime = midForm.filter('input[name="examtime"]');
    var input_aid = midForm.filter('input[name="aid"]');
    var start_timestamp;
    var mRegular = false;

    function checkMatchName() {
        var rest = input_matchname.val();
        input_matchname.next().css('color', 'red');
        if (rest.length > 5 && rest.length <= 20) {
            matchName = true;
            input_matchname.next().text('');
        } else if (!rest) {
            input_matchname.next().text('比赛名称不能为空');
        } else if (rest.length <= 5) {
            input_matchname.next().text('比赛名称太短');
        } else if (rest.length > 20) {
            input_matchname.next().text('比赛名称太长');
        }
    }

    function checkOrganame() {
        var rest = input_organame.val();
        input_organame.next().css('color', 'red');
        if (!rest) {
            input_organame.next().text('机构名称不能为空');
        } else {
            orgaName = true;
            input_organame.next().text('');
        }
    }

    function checkScore() {
        var rest = input_score.val();
        input_score.next().css('color', 'yellow');
        if (rest <= 0) {
            input_score.next().text('总分数必须大于0').end().val(1);
        } else if (rest > 1000) {
            input_score.next().text('总分数不能大于1000').end().val(50);
        } else if (Math.ceil(rest) > rest || Math.floor(rest) < rest) {
            input_score.next().text('总分数不能是小数').end().val(parseInt(rest));
        } else if (rest.match(/^0/)) {
            input_score.next().text('数字格式错误');
        } else {
            score = true;
            input_score.next().text('');
        }
    }

    function checkSubCount() {
        var rest = input_subcount.val();
        input_subcount.next().css('color', 'yellow');
        if (rest <= 0) {
            input_subcount.next().text('出题数量必须大于0').end().val(1);
        } else if (rest > num) {
            input_subcount.next().text('不能大于当前题库总题数').end().val(num);
        } else if (Math.ceil(rest) > rest || Math.floor(rest) < rest) {
            input_subcount.next().text('出题数量不能是小数').end().val(parseInt(rest));
        } else if (rest.match(/^0/)) {
            input_subcount.next().text('数字格式错误');
        } else {
            subCount = true;
            input_subcount.next().text('');
        }
    }

    function checkSetTime() {
        var rep = /20[0-9]{2}-([0,1]{1}[0-9]{1}-[0-3]{1}[0-9]{1})\s+[0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}/g;
        // var rep = /20[0-9]{2}-([0,1]{1}[0-9]{1}-[0-2]{1}[0-9]{1})|([01,03,05,07,08,10,12]{1}-3[0-1]{1})|([04,06,09,11]{1}-30)\s+[0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}/g;

        input_settime.next().css('color', 'red');
        var rest = input_settime.val();
        var rep_rest = rest.match(rep);
        if (!rest) {
            input_settime.next().text('比赛开始时间不能为空');
        } else if (!rep_rest) {
            input_settime.next().text('时间格式填写错误');
        } else if (rep_rest[0].length != rest.length) {
            input_settime.next().text('时间格式填写有误');
        } else {
            // 与当前时间作比较
            var cur_timestamp = parseInt(new Date().getTime() / 1000);
            var res = rest.replace(/-/g, '/');
            start_timestamp = parseInt(new Date(res).getTime() / 1000);
            if (cur_timestamp + 300 > start_timestamp) {
                input_settime.next().text('比赛开始时间至少须提前5分钟');
            } else {
                setTime = true;
                input_settime.next().text('');
            }
        }
    }

    function checkUsetTime() {
        var rep = /20[0-9]{2}-([0,1]{1}[0-9]{1}-[0-3]{1}[0-9]{1})\s+[0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}/g;

        input_usettime.next().css('color', 'red');
        var rest = input_usettime.val();
        var rep_rest = rest.match(rep);
        if (!rest) {
            if (!start_timestamp) {
                input_usettime.next().text('请先设置比赛的开始时间');
            } else {
                input_usettime.next().text('比赛截止时间不能为空');
            }
        } else if (!rep_rest) {
            input_usettime.next().text('时间格式填写错误');
        } else if (rep_rest[0].length != rest.length) {
            input_usettime.next().text('时间格式填写有误');
        } else {
            // 与设置开始时间作比较
            var res = rest.replace(/-/g, '/');
            var end_timestamp = parseInt(new Date(res).getTime() / 1000);
            if (end_timestamp < start_timestamp + 86400) {
                input_usettime.next().text('比赛活动时间不能低于24小时');
            } else {
                usetTime = true;
                input_usettime.next().text('');
            }
        }
    }

    function checkExamTime() {
        var rest = input_examtime.val();
        input_examtime.next().css('color', 'yellow');
        if (rest < 5) {
            input_examtime.next().text('考试时间至少5分钟').end().val(5);
        } else if (rest > num * 5) {
            input_examtime.next().text('考试时间太长对学生不好').end().val(num * 5);
        } else if (Math.ceil(rest) > rest || Math.floor(rest) < rest) {
            input_examtime.next().text('考试时间不能是小数').end().val(parseInt(rest));
        } else {
            examTime = true;
            input_examtime.next().text('');
        }
    }

    input_organame.blur(function (k) {
        checkOrganame();
    });
    input_matchname.blur(function (k) {
        checkMatchName();
    });
    input_score.blur(function (k) {
        checkScore();
    });
    input_subcount.blur(function (k) {
        checkSubCount();
    });
    input_settime.blur(function (k) {
        checkSetTime();
    });
    input_usettime.blur(function (k) {
        checkUsetTime();
    });
    input_examtime.blur(function (k) {
        checkExamTime();
    });

    // 右侧表单验证,开启信息录入功能
    function matchRegular(ths) {
        var val = $(ths).val();
        if (!val) {
            $(ths).next().text('比赛规则不能空空如也');
        } else if (val.length < 5) {
            $(ths).next().text('规则描述不能少于5个字');
        } else if (val.length > 100) {
            $(ths).next().text('规则描述不能超过100个字');
        } else {
            mRegular = true;
            $(ths).next().text('');
        }
    }

    $('.rightSet #matchRegular').blur(function (k) {
        matchRegular(this);
    });

    // 如果信息录入字段被点击，做出判断
    var otherinfoList = [];

    function checkSomeFields() {
        otherinfoList.splice(0, otherinfoList.length);
        $('.rightSet .select-field input').each(function (k) {
            if ($(this).prop('checked')) {
                otherinfoList.push($(this).attr('name'));
            }
        });
    }

    var extraInfo = $('.rightSet #addExtraInfo');
    $('.rightSet .select-field tr input').click(function (k) {
        var count = $('.rightSet .select-field tr input:checked').length;
        if(count > 5){
            alert('你有点贪心哦');
            return false;  // 取消最后的勾选
        }

        if ($(this).prop('checked')) {
            if (!extraInfo.prop('checked')) {
                extraInfo.prop('checked', true);
            }
        } else {
            var flag = false;
            $('.rightSet .select-field tr input').not($(this)).each(function () {
                if ($(this).prop('checked')) {
                    flag = true;
                }
            });
            if (!flag) {
                extraInfo.prop('checked', false);
            }
        }
        checkSomeFields();
    });

    // 点击‘+’添加下拉框字段
    $('.rightSet .glyphicon').click(function (k) {
        checkSomeFields();
        if (otherinfoList.length == 0) {
            $(this).children(':first').removeClass('hide');
            return false;
        } else {
            $(this).children(':first').addClass('hide');
        }

        // 点击add，弹出下拉菜单自定义对话框
        $('.mysetquestion .modal').show();
        $('#myModal .rightinfo, #myModal .mask').removeClass('hide');

        // 自动添加已勾选的字段
        $('.rightinfo form select option').each(function () {
            $(this).hasClass('hide') ? $(this) : $(this).addClass('hide');
        });
        for (var i in otherinfoList) {
            if (i == 0) {
                // 设置第一项为默认值
                $('.rightinfo form select option[class*=' + otherinfoList[i] + ']').attr('selected', 'selected').removeClass('hide');
                // 下拉框隐藏默认字段, 避免再次出现
            } else {
                $('.rightinfo form select option').filter('option[class*=' + otherinfoList[i] + ']').removeClass('hide');
            }
        }
    });

    // 下拉框信息不能为空
    $('.rightinfo form select').change(function (k) {
        if ($(this).val() == '姓名') {
            $(this).children().eq(0).attr('selected', true).siblings().attr('selected', false);
        } else if ($(this).val() == '性别') {
            $(this).children().eq(1).attr('selected', true).siblings().attr('selected', false);
        } else if ($(this).val() == '年龄') {
            $(this).children().eq(2).attr('selected', true).siblings().attr('selected', false);
        } else if ($(this).val() == '手机号') {
            $(this).children().eq(3).attr('selected', true).siblings().attr('selected', false);
        } else if ($(this).val() == '微信号') {
            $(this).children().eq(4).attr('selected', true).siblings().attr('selected', false);
        } else if ($(this).val() == '邮箱') {
            $(this).children().eq(5).attr('selected', true).siblings().attr('selected', false);
        } else if ($(this).val() == '身份证号') {
            $(this).children().eq(6).attr('selected', true).siblings().attr('selected', false);
        } else if ($(this).val() == '毕业院校') {
            $(this).children().eq(7).attr('selected', true).siblings().attr('selected', false);
        } else if ($(this).val() == '地址') {
            $(this).children().eq(8).attr('selected', true).siblings().attr('selected', false);
        }
        $('.rightinfo form #wantShowInfo').val('');
    });
    var wantShow = false;
    function wantShowInfo(ths) {
        var v = $(ths).val();
        if (!v) {
            $(ths).next().text('下拉框内容不能为空');
        } else if(v.startsWith('#') || v.endsWith('#')){
            $(ths).next().text('下拉框内容只能使用#分割内容，不能作为开头和结束');
        }else{
            $(ths).next().text('');
            wantShow = true;
        }
        return v;
    }

    $('.rightinfo form #wantShowInfo').blur(function (k) {
        wantShowInfo(this);
    });

    var addbody = $('.rightSet form #addField');
    $('.rightinfo .modal-footer :submit').click(function (e) {
        e.preventDefault();
        var v = wantShowInfo($('.rightinfo form #wantShowInfo'));
        if (wantShow) {
            var rightselect = $('.rightinfo form select');
            var fieldname = rightselect.val();
            var clas = rightselect.children(':selected').attr('class');
            var add_html = " <tr> <td name='"+clas+"'>" + fieldname + "</td> <td id='words-limit'><span class='words-limit'>" + v + "</span></td> <td class='del' style='cursor: pointer;'>删除</td> </tr>";

            // 判断是修改还是增加
            // 获取到的直接是子标签
            var hasname = addbody.find(":contains("+fieldname+")").length;
            if(hasname){
                var cur_tr = addbody.find(':contains('+fieldname+')');
                cur_tr.before(add_html);
                cur_tr.remove();
            }else{
                addbody.append(add_html);
            }

            $('.mysetquestion .modal').hide();
            $('#myModal .rightinfo, #myModal .mask').addClass('hide');

            wantShow = false;
        }
    });
    // 找类似1：多这样的关系
    addbody.delegate('tr .del', 'click', function (k) {
        var reldel = confirm('真的要删除吗?');
        if(reldel){
            $(this).parent().remove();
            var del = $('.rightSet form #deldelay');
            var delHtml = "<span class='deldelay'>已删除</span>";
            del.append(delHtml);
            var deltable = setTimeout(function () {
                // 删除信息
                del.children('.deldelay').eq(0).remove();
                clearTimeout(deltable);
            }, 3000);
        }
    });

    // 自定义下拉框中value值的字数限制
    function matchWordsLimit() {
        var tdWidth = $('.mysetquestion .rightSet form .addField').width();
        $('.mysetquestion .rightSet form .words-limit').width(tdWidth * 0.55 + 'px');
    }
    matchWordsLimit();

    $('.mysetquestion .saveButton').click(function (k) {
        // 检查标志位是否是true
        checkMatchName();
        checkOrganame();
        checkSubCount();
        checkScore();
        checkSetTime();
        checkUsetTime();
        checkExamTime();
        matchRegular($('.rightSet #matchRegular'));
        // 可以不检查,因为只有通过鼠标点击才能把选项加入到元组中，js操作不自动添加,但后台已做验证
        // checkSomeFields();
        if (!(matchName && orgaName && score && subCount && setTime && usetTime && examTime && mRegular)) {
            return false;
        }

        var post_url = $('.mysetquestion #matchConfig').attr('action');
        var selectLi = $('.mysetquestion .leftSet .selectKu li[class*="active"]');
        var extradict = [];
        addbody.children().each(function () {
            var addinfoTd = $(this).children(':first');
            var extraname = addinfoTd.attr('name');
            var extravalue = addinfoTd.next().text();
            extradict.push({'name': extraname, 'verbose': addinfoTd.text(), 'value': extravalue});
        });
        $.ajax({
            url: post_url,
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},  // 对于使用Ajax提交,与form中{% csrf-token %}，二选一即可
            data: {
                'qtype': selectLi.attr('type'),
                'qid': selectLi.attr('value'),
                'aid': input_aid.val(),
                // 'aid': 190,  // 不在数据库查询列表中，报错: 不在可用的选项中
                'mname': input_matchname.val(),
                'organame': input_organame.val(),
                'score': input_score.val(),
                'topicount': input_subcount.val(),
                'stime': input_settime.val(),
                'etime': input_usettime.val(),
                'mtime': input_examtime.val(),
                'mregular': $('.rightSet #matchRegular').val(),
                'extrainfo': $('.rightSet #addExtraInfo').prop('checked'),
                'otherinfo': JSON.stringify(otherinfoList),
                'choicefield': JSON.stringify(extradict)
            },
            dataType: 'json',
            type: 'post',
            traditional: true
        })
            .done(function (result) {
                var e = result.error;
                if (result.status) {
                    alert('恭喜您，比赛信息已配置成功');
                    location.href = '/match/info_' + result['obj_id'];
                } else if (e.aid) {
                    if (e.aid[0].code == 'invalid_choice') {
                        // alert(e.aid[0].message)
                        alert('用户信息被恶意篡改，你到底想干嘛？正在拨通110...')
                    } else if (e.aid[0].code == 2001) {
                        alert(e.aid[0].message + '喂，是110吗？')
                    }
                } else if (e.qtype) {
                    if (e.qtype[0].code == 2002) {
                        alert(e.qtype[0].message);
                    } else if (e.qtype[0].code == 'required') {
                        $('.mysetquestion .modal').show();
                        $('#myModal .mask, .mysetquestion #myModal .midinfo').removeClass('hide');
                    }
                } else if (e.qid) {
                    if (e.qid[0].code == 'invalid_choice') {
                        alert('喂，网警吗？我们发现...')
                    }
                } else if (e.mname) {
                    if (e.mname[0].code == 'required' || e.mname[0].code == 'min_length' || e.mname[0].code == 'max_length' || e.mname[0].code == 2005) {
                        input_matchname.next().text(e.mname[0].message);
                    }
                } else if (e.organame) {
                    if (e.organame[0].code == 'required' || e.organame[0].code == 'max_length') {
                        input_organame.next().text(e.organame[0].message);
                    }
                } else if (e.topicount) {
                    if ('required' == e.topicount[0].code || 'invalid' == e.topicount[0].code || 'min_value' == e.topicount[0].code || 'max_value' == e.topicount[0].code) {
                        input_subcount.next().text(e.topicount[0].message);
                    }
                } else if (e.score) {
                    if ('required' == e.score[0].code || 'invalid' == e.score[0].code || 'min_value' == e.score[0].code || 'max_value' == e.score[0].code) {
                        input_score.next().text(e.score[0].message);
                    }
                } else if (e.stime) {
                    if ('required' == e.stime[0].code || 'invalid' == e.stime[0].code || '2003' == e.stime[0].code) {
                        input_settime.next().text(e.stime[0].message);
                    }
                } else if (e.etime) {
                    if ('required' == e.etime[0].code || 'invalid' == e.etime[0].code || '2004' == e.etime[0].code) {
                        input_usettime.next().text(e.etime[0].message);
                    }
                } else if (e.mtime) {
                    if ('required' == e.mtime[0].code || 'invalid' == e.mtime[0].code || 'min_value' == e.mtime[0].code || 'max_value' == e.mtime[0].code) {
                        input_examtime.next().text(e.mtime[0].message);
                    }
                } else if (e.mregular) {
                    if ('required' == e.mregular[0].code || 'min_length' == e.mregular[0].code || 'max_length' == e.mregular[0].code) {
                        $('.rightSet #matchRegular').next().text(e.mregular[0].message);
                    }
                } else if (e.otherinfo) {
                    if (2006 == e.otherinfo[0].code) {
                        alert(e.otherinfo[0].message);
                    }
                } else if (e.choicefield) {
                    if (2006 == e.choicefield[0].code) {
                        alert(e.choicefield[0].message);
                    }
                } else {
                    alert('发生了未知错误，请联系管理员以尽快处理');
                }
            })
            .fail(function (k) {
                alert('服务器发生了未知错误，请联系管理员以尽快处理');
            })
    });
});

// base.html和matchconfig.html都各自一个.modal对话框,导致，遮罩层盖住模态框，自动加上行间样式：display:block;
$('.mod_passwd').click(function () {
    if($('.modal').length == 2){
        $('.modal').eq(1).css('z-index', 0);
    }
});
