/**
 * Created by uson on 19-12-5.
 */

$(function () {
    var ONAME = false;
    var OEMAIL = false;
    var OUSERNAME = false;
    var OPHONE = false;
    // 表单失效获得焦点时
    $('#organ #oemail, #organ #ousername, #organ #ousermobile, #organ #oname').focus(function () {
        $(this).next().text('');
    });
    $('#organ #m_checkcode').focus(function () {
        $('.mycontent .smse').text('');
    });
    // 邮箱输入框失去焦点时
    $('#organ #oemail').blur(function () {
        checkEmail();
    });
    function checkEmail() {
        var ths = $('#organ #oemail');
        var oemail = $(ths).val();
        var rep = /^[a-z0-9A-Z][.\w]+@[0-9a-zA-Z]+\.[a-zA-Z]+$/g;
        var res = oemail.match(rep);
        if (!oemail) {
            $(ths).next().text('邮箱必填');
        } else if (!res) {
            $(ths).next().text('请输入正确的邮箱格式')
        } else if (res[0].length != oemail.length) {
            $(ths).next().text('请输入邮箱');
        } else {
            OEMAIL = true;
        }
    }

    // 手机号输入框失去焦点时
    $('#organ #ousermobile').blur(function () {
        checkPhone();
    });
    function checkPhone() {
        var ths = $('#organ #ousermobile');
        var ophone = $(ths).val();
        var rep = /^1[3|5|7|8]{1}[0-9]{9}$/g;
        var res = ophone.match(rep);
        if (!ophone) {
            $(ths).next().text('手机号必填');
        } else if (!res) {
            $(ths).next().text('请输入正确的手机号格式');
        } else if (res[0].length != ophone.length) {
            $(ths).next().text('请输入手机号');
        } else {
            OPHONE = true;
        }
    }

    // 机构名称输入框失去焦点时
    $('#organ #oname').blur(function () {
        checkName();
    });
    function checkName() {
        var ths = $('#organ #oname');
        var oname = $(ths).val();
        if (!oname) {
            $(ths).next().text('机构名必填');
        } else if (oname[0].length > 32) {
            $(ths).next().text('机构名太长,请核实后再输入');
        } else {
            ONAME = true;
        }
    }

    // 机构联系人的校验
    $('#organ #ousername').blur(function () {
        checkUname();
    });
    function checkUname() {
        var ths = $('#organ #ousername');
        var username = $(ths).val();
        if (!username) {
            $(ths).next().text('联系人必填');
        } else {
            OUSERNAME = true;
        }
    }

    // 整体校验
    $('#organ :submit').click(function (e) {
        e.preventDefault();
        checkEmail();
        checkName();
        checkUname();
        checkPhone();
        if (!(OUSERNAME && ONAME && OPHONE && OEMAIL)) {
            return false;
        }
        var postUrl = $('#organ').attr('action');
        $.ajax({
            url: postUrl,
            data: $('#organ').serialize(),
            type: 'post',
            dataType: 'json',
            headers: {'X-CSRFtoken': $.cookie('csrftoken')}
        })
            .done(function (data) {
                console.log(data);
                if (data.status) {
                    alert('升级成功');
                    var back_url = document.referrer;
                    window.location.href = back_url;
                } else if (data.oname) {
                    $('#organ #oname').next().text(data.oname);
                } else if (data.oreluname) {
                    $('#organ #ousername').next().text(data.oreluname);
                } else if (data.oumobile) {
                    $('#organ #ousermobile').next().text(data.oumobile);
                } else if (data.oemail) {
                    $('#organ #oemail').next().text(data.oemail);
                } else if (data.m_checkcode) {
                    $('#organ .smse').text(data.m_checkcode);
                    $('.mycontent .smse').css('color', 'red');
                } else if (data.__all__[0] == '用户未登录') {
                    alert('请先登录账号，再升级机构用户');
                    location.href = postUrl + '?do=login';
                } else if (data.__all__[0] == '短信验证码错误') {
                    $('#organ .smse').text(data.__all__[0])
                    $('.mycontent .smse').css('color', 'red');
                } else if (data.__all__[0] == '验证码已过期') {
                    $('#organ .smse').text(data.__all__[0])
                    $('.mycontent .smse').css('color', 'red');
                } else{
                    $('#organ .smse').text('发生了未知的错误')
                    $('.mycontent .smse').css('color', 'red');
                }

            })
            .fail(function (data) {
                alert('服务器错误');
            })
    });

    // 短信验证码

    // 升级用户，先判断用户是否已登录,如果未登录，不发送验证码请求
    function islogin() {
        var loginStatus = $('#p_login').find('h3 a').text();  // 获取的是第一个标签的值，即手机端的那个标签
        if ('密码登录' == loginStatus) {
            return false;
        }else{
            return true;
        }
    }

    $('.mycontent .sms #get_smscode').click(function (e) {
        e.preventDefault();
        if(!islogin()){
            alert('您还没有登录哟');
            return false;
        }
        checkEmail();
        checkName();
        checkUname();
        checkPhone();
        if (!(OUSERNAME && ONAME && OPHONE && OEMAIL)) {
            return false;
        }
        var postUrl = $('#organ').attr('action');
        $.ajax({
            url: postUrl,
            data: {
                'oumobile': $('.mycontent #ousermobile').val()
            },
            dataType: 'json',
            type: 'get',
            success: function (data) {
                console.log(data);
                if (data.status) {
                    $('.mycontent .smse').text('短信发送成功, 请注意查收');
                    $('.mycontent .smse').css('color', 'green');
                } else {
                    $('.mycontent .smse').text('短信发送失败');
                }
            },
            error: function () {
                alert('服务器错误');
            }
        });
        var ltime = 59;
        var smscodeTag = $('.mycontent .sms #get_smscode');

        function getSmsCode() {
            smscodeTag.text(ltime + 's后再获取');
            if (ltime == 0) {
                clearInterval(get_code);
                smscodeTag.text('重新获取验证码');
                return false;
            }
            ltime -= 1;
        }

        var get_code = setInterval(getSmsCode, 1000);

        return false;
    });
});
