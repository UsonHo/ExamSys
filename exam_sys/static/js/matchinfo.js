/**
 * Created by uson on 19-12-29.
 */

$(function () {
    $('.main-content .report-result .close').click(function () {
        $('.main-content .report-result .modal-dialog .modal-content, .main-content .report-result .modal-dialog').addClass('hide');
    });

    $('.main-content .report-result #challage').click(function (e) {
        var num = 0;
        $('.main-content .report-result #answerUser .form-group').each(function (k) {
            var inputTag = $(this).children('input').eq(0);
            var selectTag = $(this).children('select').eq(0);
            if (!selectTag.attr('display')) {
                // select无值隐藏，检查input
                selectTag.hide();
            } else {
                // select有值，input隐藏
                num += 1;
                inputTag.attr('type', 'hidden');
                return true;
            }
            // 字符0也是真
            if (inputTag.attr('display') == 'false') {
                // input无值隐藏，隐藏div
                $(this).hide();
            } else {
                num += 1;
            }
        });
        if (num) {
            $('.main-content .report-result .modal-dialog .modal-content, .main-content .report-result .modal-dialog').removeClass('hide');
        } else {
            $('.main-content .recordSomeInfo #answerUser').submit();
        }
    });

    // 提交表单的一刹那,循环判断值是否为空
    function checkanswerInfo() {
        var value;
        $('.main-content .recordSomeInfo form .form-group span').text('');
        $('.main-content .recordSomeInfo form .form-group').each(function (k) {
            // 找到当前div标签下的input或者select标签[0：label, 1:input或者select, 2:span]
            if ($(this).find(":nth-of-type(2n+1)")[0].tagName == 'SELECT') {
                value = $(this).find(":odd :selected").text();
            } else {
                value = $(this).find(":odd").val();
            }

            if (!value) {
                $(this).children(':last').text('您还有信息没有完善哦，无法进入答题环境');
                return false;
            } else {
                return true;
            }
        });
        if (!value) {
            return false;
        } else {
            return true;
        }
    }

    function checkAnsweremail() {
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
        var email = $('.main-content .recordSomeInfo form .form-group').find('[name="uemail"]');
        if (email[0].tagName != 'SELECT') {
            if (!re.test(email.val())) {
                email.next().text('邮箱格式错误,请认真填写,系统自动识别真假用户，避免答题系统随时退出');
                return false;
            }
        }
        return true;
    }

    function checkAnswermobile() {
        var rep = /^1[3|5|7|8]{1}[0-9]{9}$/g;
        var mobile = $('.main-content .recordSomeInfo form .form-group').find('[name="umobile"]');
        if (mobile[0].tagName != 'SELECT') {
            var res = mobile.val().match(rep);
            if (!res) {
                mobile.next().text('手机格式错误,请认真填写,系统自动识别真假用户，避免答题系统随时退出');
                return false;
            }
        }
        return true;
    }

    function checkAnswerid() {
        // 函数参数必须是字符串，因为二代身份证号码是十八位，而在javascript中，十八位的数值会超出计算范围，造成不精确的结果，导致最后两位和计算的值不一致，从而该函数出现错误。
        // 详情查看javascript的数值范围
        var idcodeTag = $('.main-content .recordSomeInfo form .form-group').find('[name="uid"]');
        if (idcodeTag[0].tagName != 'SELECT') {
            var idcode = idcodeTag.val();

            // 加权因子
            var weight_factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];  // 对应前17位数字，对应相乘
            // 校验码
            var check_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
            var last = idcode[17]; // 对最后一位进行校验

            var code = idcode + "";
            var seventeen = code.substring(0, 17);  // 获取前17位

            // ISO 7064:1983.MOD 11-2
            // 判断最后一位校验码是否正确
            var arr = seventeen.split("");  // 将17位数字分开组成数组
            var len = arr.length;
            var num = 0;
            for (var i = 0; i < len; i++) {
                num += arr[i] * parseInt(weight_factor[i]);
            }

            // 获取余数
            var resisue = num % 11;
            var last_no = check_code[resisue];

            // 格式的正则
            // 正则思路
            /*
             第一位不可能是0
             第二位到第六位可以是0-9
             第七位到第十位是年份，所以七八位为19或者20
             十一位和十二位是月份，这两位是01-12之间的数值
             十三位和十四位是日期，是从01-31之间的数值
             十五，十六，十七都是数字0-9
             十八位可能是数字0-9，也可能是X
             */
            var idcard_patter = /^[1-9][0-9]{5}([1][9][0-9]{2}|[2][0][0|1][0-9])([0][1-9]|[1][0|1|2])([0][1-9]|[1|2][0-9]|[3][0|1])[0-9]{3}([0-9]|[X])$/;

            // 判断格式是否正确
            var format = idcard_patter.test(idcode);
            // console.log(idcode, format);

            // 返回验证结果，校验码和格式同时正确才算是合法的身份证号码
            // return last === last_no && format ? true : false;
            if (!(last === last_no && format)) {
                idcodeTag.next().text('身份证件不合法,不能犯罪哦');
                return false;
            }
        }
        return true;
    }

    // 提交和取消
    $('.main-content .recordSomeInfo #postInfo').click(function (e) {
        e.preventDefault();
        var formgroup = $('.main-content .recordSomeInfo form .form-group');
        if (formgroup.find('[name="uemail"]').length) {
            if (!checkAnsweremail()) {
                return false;
            }
        }
        if (formgroup.find('[name="umobile"]').length) {
            if (!checkAnswermobile()) {
                return false;
            }
        }
        if (formgroup.find('[name="uid"]').length) {
            if (!checkAnswerid()) {
                return false;
            }
        }
        if (!(checkanswerInfo())) {
            return false;
        }
        $('.main-content .recordSomeInfo #answerUser').submit();
    });
    $('.main-content .recordSomeInfo #cancleInfo').click(function (e) {
        $('.main-content .report-result .modal-dialog .modal-content, .main-content .report-result .modal-dialog').addClass('hide');
        return false;
    });

    // 时间转换
    var time_text = $('.matchinfo .res-table .second').text();
    var rep = /\d+\.\d+|\d+/g;
    var arr = time_text.match(rep);
    if (arr) {
        var rep_res = parseFloat(arr[0]);
        if (rep_res > 60) {
            $('.matchinfo .res-table .second').text('耗时：' + (rep_res / 60).toFixed(1) + ' 分钟');
        }
    }

});