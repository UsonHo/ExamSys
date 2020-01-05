/**
 * Created by uson on 19-12-5.
 */

$(function () {
    //用户注册、登录校验字段
    var NAME = false;
    var PASSWD = false;
    var CON_PASSWD = false;
    var EMAIL = false;
    var CHECKCODE = false;

    function Bug360(ths) {
        if ($(ths).css('background-color') == "rgb(250, 255, 189)") {
            $(ths).next().text('不支持当前浏览器自动填充用户信息');
            return false;
        } else {
            return true;
        }
    }

    function changeimg() {
        //当手机导航消失, 取消手机导航的菜单
        if (!$('.navbar-toggle').attr('display')) {
            $('.mob-menu').addClass('hide');
        }
    }

    changeimg();
    $(window).resize(function () {
        changeimg();
    });

    $(document).click(function () {
        $('.mob-menu').slideUp(function () {
            $(this).addClass('hide');
        });
    });

    $('#tog').click(function () {
        if ($('.mob-menu').hasClass('hide')) {
            $('.mob-menu').slideDown('fast').removeClass('hide');
        } else {
            $('.mob-menu').slideUp('fast', function () {
                $(this).addClass('hide');
            });
        }
        return false;
    });
    var mymenu = $('.mob-menu li').each(function () {
        $(this)[0].addEventListener('click', function () {
            location.href = $(this).find('a').attr('href');
        }, true);
    });
    $('.mob-menu li, a').click(function () {
        $('.mob-menu').slideUp(function () {
            $(this).addClass('hide');
        });
    });

    // 密码登录
    $('.p_login').click(function () {
        $('.register').addClass('hide');

        $('.login, .mask').removeClass('hide');
        $('.modal').show();
    });
    // 密码登录前端的一次验证
    $('#login #checkcode').focus(function () {
        // $(this).val('');
        $(this).next().text('');
    });


    $('.login #login #lemail').focus(function () {
        $(this).next().text('');
    });
    $('.login #login #lemail').blur(function () {
        check_user_email(this);
        check_loginemail(this);
    });
    function check_loginemail(ths) {
        var login_email = $(ths).val();
        if (!login_email) {
            if (!Bug360(ths)) {
                return false;
            }
            $(ths).next().text('邮箱不能为空');
        } else {
            EMAIL = true;
        }
    }

    $('.login #login #lpasswd').focus(function () {
        $(this).val('');
        $(this).next().text('');
    });
    $('.login #login #lpasswd').blur(function () {
        check_user_password(this);
        check_loginpassword(this);
    });
    function check_loginpassword(ths) {
        var login_passwd = $(ths).val();
        if (!login_passwd) {
            if (!Bug360(ths)) {
                return false;
            }
            $(ths).next().text('密码不能为空哦');
        } else {
            PASSWD = true;
        }
    }

    // 验证码v1
    $('#login #checkcode').blur(function () {
        // CHECKCODE = true;
    });
    // 验证码v2-顶象无感验证
    var myCaptcha = _dx.Captcha(document.getElementById('login_dingxiang_checkcode'), {
        appId: '3d0b7974885ff53382d3c054cee6adc3',
        success: function (token) {
            // console.log('token', token);
            var _token = $('#login input[name="token"]').val(token);
            // console.log(_token);
        }
    });

    $('#login :submit').click(function (event) {
        // 通过js设置cookie，记录登录前(当前的url路径)
        $.cookie('back_url', $('.cur_path').val());

        event.preventDefault();
        if (!(EMAIL && PASSWD)) {
            // check_user_email('#login #email');
            check_loginemail('#login #lemail');

            // check_user_password('#login #passwd');
            check_loginpassword('#login #lpasswd');
        }
        if (!(EMAIL && PASSWD)) {
            return false;
        }
        var post_url = $('#login').attr('action');
        $.ajax({
            url: post_url,
            dataType: 'json',
            type: 'post',
            data: $('#login').serialize(),
            headers: {'X-CSRFtoken': $.cookie('csrftoken')}
        })
            .done(function (data) {
                if (data.status) {
                    if (data.url != '/') {
                        // console.log(data);
                        location.href = data.url;
                        // window.location.href = document.referrer;  // 多返回了一个url,即回到了点击需要登录页面之前的那个页面
                    }else{
                        location.href = $.cookie('back_url');
                    }
                } else if (data.field == 'email') {
                    $('#login #lemail').next().text(data.error_msg);
                } else if (data.field == 'passwd') {
                    $('#login #lpasswd').next().text(data.error_msg);
                } else if (data.field == 'checkcode') {
                    alert(data.error_msg);
                }
            })
            .fail(function () {
                //
            })
    });


    //找回密码
    $('.find-passwd #femail').focus(function () {
        $(this).next().text('');
    });

    $('#resetPasswd, .mod_passwd').click(function () {
        $('.login').addClass('hide');

        $('.find-passwd').removeClass('hide');
    });

    $('.find-passwd :submit').click(function (event) {
        event.preventDefault();

        if (!(EMAIL && PASSWD && CON_PASSWD && CHECKCODE)) {
            check_loginemail($('.find-passwd #femail'));
            check_user_password($('.find-passwd #new-passwd'));
            check_confirmPassword($('.find-passwd #confirm-new-passwd'));

            if (!$('.find-passwd #find_pwd_code').val()) {
                $('.find-passwd #find_pwd_code').next().text('验证码不能为空');
                CHECKCODE = false;
                return;
            }
        }

        var post_url = $('#findpwd').attr('action');
        $.post(post_url, {
            femail: $('.find-passwd #femail').val(),
            new_passwd: $('.find-passwd #new-passwd').val(),
            confirm_passwd: $('.find-passwd #confirm-new-passwd').val(),
            captcha_0: $('#id_reg_captcha_0').val(),
            captcha_1: $('.find-passwd #find_pwd_code').val(),
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        }, function (result) {
            // console.log(123); 后
            console.log(result);
            if (result.status) {
                alert('邮件发送成功, 请立即登录邮箱进行激活!');
                location.href = 'https://mail.qq.com/'
            } else if (result.captcha) {
                $('.find-passwd #find_pwd_code').next().text(result.captcha[0]);
            } else if (result.femail) {
                $('.find-passwd #femail').next().text(result.femail[0])
            } else {
                alert('邮件发送失败');
            }
            /*
             $.getJSON("/captcha/refresh/", function (result) {
             $('.captcha').attr('src', result['image_url']);
             $('#id_reg_captcha_0').val(result['key']);
             });
             */
            autogetFindpwdCode();
        });
        // console.log(999); 先
    });
    // 自动获取验证码图片
    function autogetFindpwdCode() {
        $.getJSON("/captcha/refresh/", function (result) {
            $('.captcha').attr('src', result['image_url']);
            $('#id_reg_captcha_0').val(result['key']);
        });
    }

    autogetFindpwdCode();


    // 用户注册篇
    $('#signUp').click(function (event) {
        $('.login').addClass('hide');
        $('.register').removeClass('hide');
    });
    // 用户名第一层验证
    function focusEmptyEvent(ths) {
        $(ths).next().text('');
        $(ths).val('');
    }

    function focusNotEmpty(ths) {
        $(ths).next().text('');
    }

    $('.register #name').focus(function () {
        focusNotEmpty(this);
    });
    $('.register #passwd').focus(function () {
        focusEmptyEvent(this);
    });
    $('.register #confirm-passwd').focus(function () {
        focusEmptyEvent(this);
    });
    $('.register #email').focus(function () {
        focusNotEmpty(this);
    });
    $('.find-passwd #new-passwd').focus(function () {
        focusEmptyEvent(this);
    });
    $('.find-passwd #confirm-new-passwd').focus(function () {
        focusEmptyEvent(this);
    });
    $('.register #checkcode').focus(function () {
        focusEmptyEvent(this);
    });
    $('.find-passwd #find_pwd_code').focus(function () {
        focusEmptyEvent(this);
    });
    $('.register #name').blur(function () {
        check_user_name(this);
    });
    function check_user_name(ths) {
        var name = $(ths).val();
        // console.log(name);
        var nameLen = name.length;
        if (nameLen >= 4 && nameLen <= 10) {
            var rep = /^[a-zA-Z][^\W+_]+/g;
            var repname = name.match(rep);
            if (repname != null) {

                if (repname[0].length == name.length) {
                    // console.log(repname);
                    NAME = true;
                    // $(ths).next().text('输入合法');
                } else {
                    $(ths).next().text('用户名字符输入不合法')
                }

            } else {
                $(ths).next().text('用户名必须以字母开头');
            }
        } else {
            $(ths).next().text('用户名长度输入不合法');
            if (!Bug360(ths)) {
                return false;
            }
        }
    }

    //密码验证
    $('.register #passwd').blur(function () {
        check_user_password(this);
    });
    $('.find-passwd #new-passwd').blur(function () {
        check_user_password(this);
    });
    $('.find-passwd #confirm-new-passwd').blur(function () {
        check_user_password(this);
    });
    function check_user_password(ths) {
        var passwd = $(ths).val();
        if (passwd.length >= 6) {
            PASSWD = true;
        } else {
            $(ths).next().text('密码长度太短');
            if (!Bug360(ths)) {
                return false;
            }
        }
    }

    // 二次密码输入验证
    $('.register #confirm-passwd').blur(function () {
        check_confirmPassword(this);
    });
    $('.find-passwd #confirm-new-passwd').blur(function () {
        check_confirmPassword(this);
    });
    function check_confirmPassword(ths) {
        var con_passwd = $(ths).val();
        // var passwd = $('.register #passwd').val();
        var passwd = $(ths).parent().prev().children('input[type="password"]').val();
        // console.log(con_passwd, passwd);
        if (passwd != con_passwd) {
            $(ths).next().text('两次密码输入不一致')
        } else {
            CON_PASSWD = true;
        }
    }

    // 验证码验证
    $('.register #checkcode').blur(function () {
        check_code(this);
    });
    function check_code(ths) {
        var checkcode = $(ths).val();
        if (checkcode != null) {
            if (checkcode.length == 4) {
                CHECKCODE = true;
            } else {
                $(ths).next().text('验证码长度错误');
            }
        } else {
            $(ths).next().text('验证码必填');
        }
    }

    // 邮箱的验证
    function check_email() {
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        if (re.test($('#email').val())) {
            $('#email').next().hide();
        }
        else {
            $('#email').next().html('你输入的邮箱格式不正确');
            $('#email').next().show();
        }

    }

    $('.register #email').blur(function () {
        check_user_email(this);
        // check_email();
    });
    $('.find-passwd #femail').blur(function () {
        check_user_email(this);
    });

    function check_user_email(ths) {
        var email = $(ths).val();
        var rep = /^[a-z0-9A-Z][.\w]+@[0-9a-zA-Z]+\.[a-zA-Z]+/g;  // mr.uson@gmail.com
        var repemail = email.match(rep);
        if (repemail != null) {
            if (repemail[0].length != email.length) {
                $(ths).next().text('邮箱格式输入不正确');
            } else {
                EMAIL = true;
            }
        } else {
            $(ths).next().text('请输入邮箱');
            if (!Bug360(ths)) {
                return false;
            }
        }
    }

    $('.register .modal-footer :submit').click(function (event) {

        // 用户注册表单验证
        event.preventDefault();
        if (!(NAME && PASSWD && CON_PASSWD && CHECKCODE && EMAIL)) {
            console.log('必填验证');
            check_user_email($('.register #email'));
            check_code($('.register #checkcode'));
            check_user_name($('.register #name'));
            check_user_password($('.register #passwd'));
            check_confirmPassword($('.register #confirm-passwd'));
            return;
        }
        var post_url = $('#register').attr('action');
        $.ajax({
            url: post_url,
            type: 'POST',
            dataType: 'JSON',
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            data: $('#register').serialize()
        })
            .done(function (data) {
                // console.log(data, data.checkcode[0]);
                if (data.status) {
                    alert('用户注册成功');
                    // $('#register').submit();
                    location.href = '/';
                } else if (data.uname) {
                    $('.register #name').next().text(data.uname);
                } else if (data.uemail) {
                    $('.register #email').next().text(data.uemail);
                } else if (data.con_passwd) {
                    $('.register #confirm-passwd').next().text(data.con_passwd);
                } else if (data.checkcode.length > 0) {
                    $('.register #checkcode').next().text(data.checkcode[0]);
                }
                console.log('结束');
            })
            .fail(function () {
                console.log('服务器错误500');
            });
    });

    //关闭模态框
    $('.close').click(function () {
        $(this).closest('.modal-content').addClass('hide');
        $('.modal').hide();
        $('.mask').addClass('hide');
    });

    // 基于第二种方式-用户注册时动态获取获取验证码
    $('#dynamic_checkcode').click(function () {
        this.src = this.src + '?';
    });

    // 基于第三种方式-pypi模块安装-用于找回密码
    $('.captcha').click(function () {
        $.getJSON("/captcha/refresh/", function (result) {
            $('.captcha').attr('src', result['image_url']);
            $('#id_reg_captcha_0').val(result['key'])
        });
    });

    // 密码重置结果
    var res_resetpwd = $('.modal .resetpwd_result').text();
    if (res_resetpwd == 'success') {
        alert('密码重置成功');
    } else if (res_resetpwd == 'invalid') {
        alert('链接已失效');
    }

    // 根据后端url跳转，打开指定的模态框
    var cur_path = $('.cur_path').val().split('=')[1];
    if (cur_path == 'login') {
        var loginStatus = $('#p_login').find('h3 a').text();  // 获取的是第一个标签的值，即手机端的那个标签
        if ('密码登录' == loginStatus) {
            $('.register').addClass('hide');
            $('.login, .mask').removeClass('hide');
            $('.modal').show();
        } else {
            alert('你已登录');
        }
    }
});