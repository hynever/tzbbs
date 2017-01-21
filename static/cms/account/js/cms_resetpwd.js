/**
 * Created by Administrator on 2016/12/17.
 */


$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var oldpwd_input = $('input[name="oldpwd"]');
        var newpwd1_input = $('input[name="newpwd1"]');
        var newpwd2_input = $('input[name="newpwd2"]');

        var oldpwd = oldpwd_input.val();

        if(!oldpwd){
            xtalert.alertInfoToast('请输入原始密码');
            return;
        }

        var newpwd1 = newpwd1_input.val();

        if(!newpwd1){
            xtalert.alertInfoToast('请输入新密码');
            return;
        }

        var newpwd2 = newpwd2_input.val();

        if(!newpwd2){
            xtalert.alertInfoToast('请输入确认密码');
            return;
        }

        console.log('coming...');


        xtajax.post({
            'data': {
                'oldpwd': oldpwd,
                'newpwd1': newpwd1,
                'newpwd2': newpwd2,
            },
            'success': function (data) {
                if(data['code'] != 200){
                    xtalert.alertInfoToast(data['message']);
                }else{
                    xtalert.alertSuccessToast('修改成功！');
                }
                // 清除value
                oldpwd_input.val('');
                newpwd1_input.val('');
                newpwd2_input.val('');
            },
        });
    });
});