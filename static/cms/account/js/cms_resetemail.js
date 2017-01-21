/**
 * Created by Administrator on 2016/12/19.
 */


$(function () {
    // 发送邮件
    $('#send-mail-btn').click(function (event) {
        event.preventDefault();
        // 获取当前的邮箱
        var email = $('input[name="email"]').val();

        if(!email){
            xtalert.alertInfoToast('请输入邮箱！');
            return;
        }

        // 调用发送邮件的接口
        xtajax.get({
            'url': '/common/email_captcha/',
            'data': {
                'email': email
            },
            'success':function (data) {
                if(data['code'] != 200){
                    console.log(data['message']);
                    xtalert.alertInfoToast(data['message']);
                }else{
                    //清除数据
                    xtalert.alertSuccessToast('验证码已发送！');
                }
            },
            'error': function (error) {
                xtalert.alertNetworkError();
            }
        });
    });
});


// 修改邮箱的点击方法
$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var email = $('input[name="email"]').val();
        var captcha = $('input[name="captcha"]').val();

        if(!email){
            xtalert.alertInfoToast('请输入邮箱');
            return;
        }

        if(!captcha){
            xtalert.alertInfoToast('请输入验证码');
            return;
        }

        xtajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if(data['code'] != 200){
                    xtalert.alertInfoToast(data['message']);
                }else{
                    xtalert.alertSuccessToast('邮箱修改成功！');
                    $('input[name="email"]').val('');
                    $('input[name="captcha"]').val('');
                }
            },
            'error': function (error) {
                xtalert.alertNetworkError();
            }
        })
    });
});