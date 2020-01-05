/**
 * Created by uson on 19-12-31.
 */

$(function () {
    $('.matchdetail .main-content .test-body .topicTitle').each(function (k) {
        var value = $(this).text();
        var rep = /##/g;
        if (rep.test(value)) {
            var s = Math.pow(10, 5).toString().replace(/1|0/g, '_');
            $(this).text(($(this).text()).replace(rep, s));
        }
    });

    // 倒计时
    var timeTag = $('.matchdetail .testing .test-lefttime span');
    var totalTime = parseInt(timeTag.text());

    var hour = parseInt(totalTime / 60);
    var mini = parseInt(totalTime % 60) - 1;
    var sec = 60;
    var totalSec = totalTime * 60;
    var notice = false;

    // 定时器设置每100s，只要切换标签，定时器就会暂停
    function calcTime() {
        totalSec -= 1;
        if (totalSec < 0) {
            clearInterval(leftTime);  // 这里无法访问leftTime局部变量, 需要先在外部定义
            // 还可以通过以下windows对象实现清除定时器
            // stoptimer();

            notice = confirm('您已超时，未能成功交卷');
            window.history.back();
        } else if (totalSec <= 300 && !notice) {
            // notice = confirm('距离考试结束时间不到5分钟了,超时将无法交卷。');  // 有问题，阻止js代码往下继续执行，即时间暂停
        }

        hour = parseInt(totalSec / 3600);
        mini = parseInt(totalSec % 3600 / 60);
        sec = parseInt(totalSec % 60);
        timeTag.text(hour + '时' + mini + '分' + sec + '秒');
    }

    calcTime();
    var leftTime;

    function starttimer() {
        leftTime = setInterval(calcTime, 1000);
        // 这里函数调用不能加括号和‘’,可能是因为是引用的js文件的原因吧，{{}}模板语言在外部js中也不生效
    }

    starttimer();
    function stoptimer() {
        window.clearInterval(leftTime);
    }

    /*
     有问题：切换页面标签时，该时间暂停
     var leftTime = setInterval(function () {
     totalSec -= 0.1;
     hour = parseInt(totalSec / 3600);
     mini = parseInt((totalSec - hour * 3600) / 60);
     sec = totalSec - hour * 3600 - mini * 60;
     timeTag.text(hour+'时'+mini+'分'+Math.ceil(sec)+'秒');
     }, 100);
     */

    // 初始化页面
    var pagenation = $('.matchdetail .main-content .pagenation');
    pagenation.addClass('hide');
    pagenation.eq(0).removeClass('hide');
    var max_index = pagenation.length - 1;

    function checkPrevPage() {
        var current_index = pagenation.filter('[class="pagenation"]').index();
        if (current_index == 0) {
            $('.matchdetail .main-content #prevpage').hide().siblings().show();
            return current_index;
        } else {
            $('.matchdetail .main-content button').show();
            return current_index - 1;
        }
    }

    checkPrevPage();
    function checkNextPage() {
        var current_index = pagenation.filter('[class="pagenation"]').index();
        if (current_index == max_index) {
            $('.matchdetail .main-content #nextpage').hide().siblings().show();
            return current_index;
        } else {
            $('.matchdetail .main-content button').show();
            return current_index + 1;
        }
    }

    checkNextPage();
    $('.matchdetail .main-content #prevpage').hide();

    $('.matchdetail .main-content form .radio input').click(function (e) {
        $(this).attr('checked', true).parent().parent().siblings().find('input').attr('checked', false);
    });

    $('.matchdetail .main-content button').on('click', function (e) {
        var bisiness, current_index, answer, title;
        var post_url = $('.matchdetail .main-content form').attr('action');

        if ($(this).text() == '前进') {
            // bisiness = 'next_page';
            current_index = checkNextPage();
            pagenation.eq(current_index).removeClass('hide').siblings().addClass('hide');
            checkNextPage();
            return false;
        } else if ($(this).text() == '后退') {
            // bisiness = 'prev_page';
            current_index = checkPrevPage();
            pagenation.eq(current_index).removeClass('hide').siblings().addClass('hide');
            checkPrevPage();
            return false;
        }
        var all_title_answer = [];
        var tType;
        pagenation.each(function (k) {
            title = $(this).find('.topicTitle').text();
            // 将title中的_再转回##
            var rep = /[_]{6}/g;
            title = title.replace(rep, '##');

            if ($(this).find('form div').hasClass('form-group')) {
                answer = $(this).find('form .form-group input').val();
                tType = {'title': title, 'answer': answer, 'type': 'fb'};
            } else {
                var res = $(this).find('form .radio input:checked');
                if (res) {
                    answer = res.parent().text();
                } else {
                    answer = '';
                }
                tType = {'title': title, 'answer': answer, 'type': 'ch'};
            }
            all_title_answer.push(tType);
        });
        $.ajax({
            url: post_url,
            type: 'post',
            dataType: 'json',
            data: {
                'exam': JSON.stringify(all_title_answer)
                // 'bisiness': bisiness
            },
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            traditional: true,
            success: function (data) {
                console.log(data);
                if (data.error) {
                    alert(data.error)
                } else {
                    alert('交卷成功');
                }
                window.location.href = document.referrer;  // 可以刷新页面
                // window.history.back(); # 不刷新页面
                // location.href = furl + '-' + pindex + '/'; 这里跳转全是get请求
            },
            error: function () {
                //
            }
        })
    });
});
