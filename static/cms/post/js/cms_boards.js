/**
 * Created by Administrator on 2016/12/20.
 */

// 删除板块
$(function () {
   $('.delete-btn').click(function () {
       var self = $(this);
       xtalert.alertConfirm({
           'msg': '您确定要删除本板块吗？',
           'confirmCallback': function () {
               // 发送ajax请求
               xtajax.post({
                   'url': '/cms/delete_board/',
                   'data':  {
                       'id': self.attr('data-board-id')
                   },
                   'success': function (data) {
                       if(data['code'] != 200){
                           setTimeout(function () {
                               xtalert.alertInfoToast(data['message']);
                           },1000);
                       }else{
                           xtalert.alertSuccessToast('删除成功！');
                           window.location.reload();
                       }
                   }
               });
           }
       });
   });
});


// 添加板块
$(function () {
    $('#add-board-btn').click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'text': '请输入板块名称',
            'confirmCallback': function (inputValue) {
                // 发送ajax请求
                xtajax.post({
                    'url': '/cms/boards/add_board/',
                    'data':{
                        'name': inputValue,
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            xtalert.alertInfoToast(data['message']);
                        }else{
                            xtalert.alertSuccessToast('添加成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },1000);
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

// 编辑板块
$(function () {
   $('.edit-board-btn').click(function (event) {
       event.preventDefault();
       var self = $(this);
       xtalert.alertOneInput({
           'text': '请输入板块名称',
           'confirmCallback': function (inputValue) {
               // 发送ajax请求
                xtajax.post({
                    'url': '/cms/boards/edit_board/',
                    'data':{
                        'name': inputValue,
                        'id': self.attr('data-board-id')
                    },
                    'success': function (data) {
                        if(data['code'] != 200){
                            xtalert.alertInfoToast(data['message']);
                        }else{
                            xtalert.alertSuccessToast('添加成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },1000);
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