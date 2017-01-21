/**
 * Created by Administrator on 2016/12/26.
 */

// 加入黑名单
$(function () {
    $('#add-backlist-btn').click(function () {
        var self = $(this);
        var user_id = self.attr('data-user-id');
        xtalert.alertConfirm({
            'msg': '您确定要将此用户加入黑名单吗？',
            'confirmCallback': function () {
               // 发送ajax请求
                xtajax.post({
                    'url': '/cms/users/add_backlist/',
                    'data': {
                        'id': user_id
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            console.log(data);
                            xtalert.alertInfoToast(data['message']);
                        }else{
                            xtalert.alertSuccessToast('已加入黑名单！');
                            window.location.reload();
                        }
                    }
                });
            }
        });
    });
});


// 移出黑名单
$(function () {
    $('#remove-backlist-btn').click(function () {
        var self = $(this);
        var user_id = self.attr('data-user-id');
        xtalert.alertConfirm({
            'msg': '您确定要将此用户移出黑名单吗？',
            'confirmCallback': function () {
               // 发送ajax请求
                xtajax.post({
                    'url': '/cms/users/remove_backlist/',
                    'data': {
                        'id': user_id
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            xtalert.alertInfoToast(data['message']);
                        }else{
                            xtalert.alertSuccessToast('已移出黑名单！');
                            window.location.reload();
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $('#submit-btn').click(function (event) {
        var self = $(this);
        event.preventDefault();
        // 获取所有的分组
        var roleInputs = $('.role-group input[type=checkbox]:checked');
        console.log(roleInputs);
        var roles = [];
        roleInputs.each(function (index,element) {
            roles.push($(element).val());
        });

        // 发送ajax请求
        xtajax.post({
            'url': '/cms/users/edit_user/',
            'data': {
                'roles[]': roles,
                'id': self.attr('data-user-id')
            },
            'success': function (data) {
                if(data['code'] != 200){
                    console.log(data);
                    xtalert.alertInfoToast(data['message']);
                }else{
                    xtalert.alertSuccessToast('更新成功！');
                    setTimeout(function () {
                        window.location = '/cms/users/'
                    },1000);
                }
            }
        });
    });
});
