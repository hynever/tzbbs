/**
 * Created by Administrator on 2016/12/13.
 */

//提交按钮执行事件
$(function () {
   $('#submit-btn').click(function (event) {
       event.preventDefault();

       // 获取当前的标题
       var title = $('#title-input').val();

       if(title.length < 3 || title.length > 100){
           xtalert.alertInfo('标题字数应该在3-100之间！');
           return;
       }

       //获取当前的帖子
       var content = editor.$txt.html();
       var content_txt = editor.$txt.text();
       if(content_txt.length < 10) {
           xtalert.alertInfo('帖子内容不少于10个文字！');
           return;
       }else if(content_txt.length > 10000){
           xtalert.alertInfo('帖子内容不多于10000个文字');
           return;
       }

       //获取当前验证码
       var captcha = $('#captcha-input').val();

       if(captcha.length != 4){
           xtalert.alertInfo('验证码错误！');
           return;
       }

       //获取当前选中的板块
       var board = $('#board-select').val();

       //判断当前是否已经还有没有上传的文件
       if($('#upload-btn').attr('disabled')){
           xtalert.alertInfoToast('请等待文件上传完成！');
           return;
       }


       //通过ajax发送数据到后台
       xtajax.post({
           'data': {
               'title': title,
               'content': content,
               'captcha': captcha,
               'board_id': board
           },
           'success': function (data) {
               if(data['code'] != 200){
                   xtalert.alertInfoToast(data['message']);
                   //重新刷新验证码
                   refreshCaptcha();
               }else{
                   // 弹出一个模态对话框提示成功
                   xtalert.alertConfirm({
                       'msg': '恭喜！帖子发表成功！',
                       'confirmText': '再发一篇',
                       'cancelText': '回到首页',
                       'confirmCallback':function () {
                           console.log('confirmCallback');
                           window.location.reload();
                       },
                       'cancelCallback':function () {
                           console.log('coming...');
                           window.location = '/';
                       }
                   });
               }
           },
           'error': function (err) {
               xtalert.alertNetworkError();
           }
       });
   });
});

//绑定点击验证码按钮的执行事件
$(function () {
   $('#captcha-img').click(function (event) {
       event.preventDefault();
       refreshCaptcha();
   });
});

// 刷新验证码
function refreshCaptcha() {
    var captcha_img = $('#captcha-img');
    var old_src = captcha_img.attr('src');
    var src = old_src + '?xx=' + Math.random();
    captcha_img.attr('src',src);
}