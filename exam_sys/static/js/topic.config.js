/**
 * Created by uson on 19-12-19.
 */

$(function () {
    // 表单验证
    var topicName_error = true;
    var topicType_error = false;
    var topicFile_error = true;

    var topic_name = $('.main-content .topic-operate #topicName');
    var topic_type = $('.main-content .topic-operate #topicType');
    var topic_file = $('.main-content .topic-operate #topicFile');

    function checkTopicName() {
        topic_name.blur();
    }

    topic_name.blur(function () {
        if (!$(this).val()) {
            $(this).next().text('题库名不能为空');
        } else {
            $(this).next().text('');
            topicName_error = false;
        }
    });

    function checkTopicType() {
        if ("请选择一个题库类型" != topic_type.text()) {
            topic_type.parent().next().text('');
            topicType_error = false;
        } else {
            topic_type.parent().next().text('请选择一个题库');
        }
    }

    function checkTopicFile() {
        if (topic_file.val()) {
            topicFile_error = false;
            $(this).next().text('');
        } else {
            topic_file.next().text('请上传题库');
        }
    }

    topic_file.change(function () {
        if ($(this).val()) {
            $(this).next().text('');
        }
    });

    // 自动生成题库类型
    var options = $('.main-content .topic-operate .dropdown-menu option');
    var myspan = $('.main-content .topic-operate .dropdown span');
    options.each(function (k) {
        $(this).addClass('dropdown-item form-control');
    });
    $('.main-content .topic-operate .dropdown-menu').delegate('option', 'click', function (event) {
        // $(this).prop('selected', true).siblings().prop('selected', false);
        $(this).attr('name', 'qtype').siblings().removeAttr('name');
        var topicType = $(this).text();
        myspan.text(topicType);

        // 选中之后，把错误提示内容也清空了
        topic_type.parent().next().text('');
    });

    // 提交表单题库信息
    /*
     $('.form-set').submit(function (e) {
     // console.log(e);
     // 此时还没有真正的提交表单, 也不能提交option中的内容
     checkTopicName();
     checkTopicType();
     checkTopicFile();

     if (!topicName_error && !topicType_error && !topicFile_error) {
     return true;
     } else {
     return false;
     }
     });
     */

    $('#form-set button[type="submit"]').click(function (e) {
        e.preventDefault();
        // 负责输入错误提示以及重置标志位
        checkTopicName();
        // checkTopicType();
        checkTopicFile();

        if (!topicName_error && !topicType_error && !topicFile_error) {
            var post_url = $('#form-set').attr('action');
            var fd = new FormData();
            var file_obj = $('#topicFile')[0].files[0];
            fd.append('qfile', file_obj);
            fd.append('aid', $('.topic-operate input[name="aid"]').val());
            fd.append('qname', topic_name.val());
            fd.append('qtype', $('.main-content .topic-operate .dropdown-menu option[name="qtype"]').val());

            $.ajax({
                url: post_url,
                type: 'post',
                headers: {'X-CSRFtoken': $.cookie('csrftoken')},
                data: fd,
                processData: false,
                contentType: false,
                dataType: 'json'
            })
                .done(function (data) {
                    console.log(data);
                    if(data.status){
                        $('.topic-operate #form-set').addClass('hide');
                        $('.topic-operate .create_success').removeClass('hide');
                        $('.topic-operate #cnum').text(data.qselect);
                        $('.topic-operate #fnum').text(data.qfillblank);
                        $('.topic-operate #rcnum').text(data.repeat_choice);
                        $('.topic-operate #rfnum').text(data.repeat_fillbank);
                    }else if(data.qfile[0].code == '1002'){
                        topic_name.next().text(data.qfile[0].message);
                    }else if(data.qfile[0].code == '1001'){
                        topic_file.next().text(data.qfile[0].message);
                    }else if(data.qfile[0].code == '1003'){
                        topic_file.next().text(data.qfile[0].message);
                    }else if(data.qfile[0].code == '1004'){
                        topic_file.next().text(data.qfile[0].message);
                    }else if(data.qfile[0].code == '1005'){
                        topic_file.next().text(data.qfile[0].message);
                    }else if(data.qfile[0].code == '1006'){
                        topic_file.next().text(data.qfile[0].message);
                    }else if(data.qfile[0].code == '1007'){
                        topic_file.next().text(data.qfile[0].message);
                    }
                });
        }
    });
});
