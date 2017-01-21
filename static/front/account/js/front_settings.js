// 选择头像
$(function () {
    var captchaImg = $('#avatar-img');
    xtqiniu.setUp({
        'browse_btn': 'avatar-img',
        'fileadded': function () {
            captchaImg.attr('alt','图片上传中...');
        },
        'success': function (up,file,info) {
            $('#avatar-img').attr('src',file.name);
        }
    });
});

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var username = $('input[name="username"]').val();
        var realname = $('input[name="realname"]').val();
        var qq = $('input[name="qq"]').val();
        var signature = $('#signature-area').val();
        var avatar = $('#avatar-img').attr('src');

        xtajax.post({
            'url': '/account/settings/',
            'data': {
                'id': self.attr('data-user-id'),
                'username': username,
                'realname': realname,
                'qq': qq,
                'signature': signature,
                'avatar': avatar
            },
            'success': function (data) {
                if(data['code'] != 200){
                    xtalert.alertInfoToast(data['message']);
                }else{
                    xtalert.alertSuccessToast('保存成功！');
                }
            }
        });

    });
});
