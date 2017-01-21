/**
 * Created by Administrator on 2016/12/26.
 */

$(function () {
    $('input[name="public"]').click(function () {
        var self = $(this);
        $('#role-group').slideToggle();
    });
});
$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        // 获取板块名称
        var nameInput = $('input[type="text"][name="name"]');
        var name = nameInput.val();

        if(!name){
            xtalert.alertInfo('请输入板块名称！');
            return;
        }

        var roles = [];
        var publicInput = $('input[name="public"]');
        var isPublic = publicInput.is(':checked');
        var checkboxs = $('.role-checkbox').filter(':checked');
        if(!isPublic){
            checkboxs.each(function (index,element) {
                roles.push($(element).val());
            });
        }

        // 发送ajax请求
        xtajax.post({
            'url': '/cms/boards/add_board/',
            'data':{
                'name': name,
                'roles[]': roles
            },
            'success': function (data) {
                if(data['code'] != 200){
                    xtalert.alertInfoToast(data['message']);
                }else{
                    // 清除这个页面
                    nameInput.val('');
                    checkboxs.each(function () {
                        $(this).removeAttr('checked');
                    });
                    // 弹出成功框
                    xtalert.alertSuccessToast('添加成功！');
                }
            },
            'error': function () {
                xtalert.alertNetworkError();
            }
        })
    });
});
