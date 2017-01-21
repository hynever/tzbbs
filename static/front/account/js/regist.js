/**
 * Created by Administrator on 2016/12/21.
 */


$(function () {
    $('#telphone-captcha-btn').click(function (event) {
        event.preventDefault();
        var telphone = $('input[name="telphone"]').val();
        if(!telphone){
            xtalert.alertInfoToast('请输入手机号码！');
            return;
        }
        var self = $(this);
        var timeCount = 60;
        self.attr('disabled','disabled');
        // 设置当前倒计时
        var timer = setInterval(function () {
            self.text(timeCount);
            timeCount--;
            if(timeCount <= 0){
                self.text('获取验证码');
                self.removeAttr('disabled');
                clearInterval(timer);
            }
        },1000);
        // 发送ajax的请求
        xtajax.get({
            'url': '/common/telphone_captcha/',
            'data': {
                'telphone': telphone
            },
            'success': function (data) {
                if(data['code'] != 200){
                    xtalert.alertInfoToast(data['message'])
                }else{
                    var msg = '验证码已发送至'+email+'，请注意查收！';
                    xtalert.alertSuccessToast(msg)
                }
            }
        });
    });
});