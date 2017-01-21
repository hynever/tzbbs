/**
 * Created by Administrator on 2016/12/21.
 */


// 添加角色按钮点击事件
$(function () {
    $('#add-role-btn').click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'title': '添加分组',
            'text': '请输入分组名称',
            'confirmCallback': function (inputValue) {
                // 发送ajax请求
                xtajax.post({
                    'url': '/cms/add_role/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            xtalert.alertInfoToast(data['messaage']);
                        }else{
                            xtalert.alertSuccessToast('添加成功！');
                            setTimeout(function () {
                                // 重新加载整个页面
                                window.location.reload();
                            },1000);
                        }
                    }
                });
            }
        });
    });
});


// 编辑角色按钮点击事件
$(function () {
    $('.edit-btn').click(function () {
        var self = $(this);
        // 弹出对话框
        xtalert.alertOneInput({
            'title': '编辑分组',
            'text': '请输入分组名称',
            'confirmCallback': function (inputValue) {
                // 发送ajax请求
                var role_id = self.attr('data-role-id');
                xtajax.post({
                    'url': '/cms/edit_role/',
                    'data': {
                        'id': role_id,
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            xtalert.alertInfoToast(data['message']);
                        }else{
                            xtalert.alertSuccessToast('修改成功！');
                            // 重新加载这个页面
                            window.location.reload();
                        }
                    },
                    'error': function () {
                        xtalert.alertNetworkError();
                    }
                });
            }
        });
    });
});

// 删除分组按钮点击事件
$(function () {
    $('.delete-btn').click(function () {
        var self = $(this);
        xtalert.alertConfirm({
            'msg': '您确定要删除这个分组吗？',
            'confirmCallback': function () {
                // 发送ajax请求
                xtajax.post({
                    'url': '/cms/delete_role/',
                    'data': {
                        'id': self.attr('data-role-id')
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            setTimeout(function () {
                                xtalert.alertInfoToast(data['message']);
                            },500);
                        }else{
                            xtalert.alertSuccessToast('删除成功！');
                            window.location.reload();
                        }
                    },
                    'error': function () {
                        xtalert.alertNetworkError();
                    }
                })
            }
        })
    });
});