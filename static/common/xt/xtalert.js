/**
 * Created by Administrator on 2016/12/14.
 */

var xtalert = {
    'alertError': function (msg) {
        swal('提示',msg,'error');
    },
    'alertInfo':function (msg) {
        swal('提示',msg,'warning');
    },
    'alertInfoWithTitle': function (title,msg) {
        swal(title,msg);
    },
    'alertSuccessWithTitle':function (title,msg) {
        swal(title,msg,'success');
    },
    'alertSuccess':function (msg,confirmCallback) {
        args = {
            'title': '提示',
            'text': msg,
            'type': 'success',
        }
        swal(args,confirmCallback);
    },
    'alertWarning':function (msg) {
        swal({
            'title': '',
            'type': 'warning',
            'showCancelButton': true,
            'confirmButtonText': '确定',
        });
    },
    'alertNetworkError':function () {
        this.alertErrorToast('网络错误！');
    },
    'alertConfirm':function (params) {
        swal({
            'title': '提示',
            'showCancelButton': true,
            'showConfirmButton': true,
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : '确定',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : '取消',
            'text': params['msg'] ? params['msg'] : ''
        },function (isConfirm) {
            if(isConfirm){
                if(params['confirmCallback']){
                    params['confirmCallback']();
                }
            }else{
                if(params['cancelCallback']){
                    params['cancelCallback']();
                }
            }
        });
    },
    'alertOneInput': function (params) {
        swal({
            'title': params['title'] ? params['title'] : '请输入',
            'text': params['text'] ? params['text'] : '',
            'type':'input',
            'showCancelButton': true,
            'animation': 'slide-from-top',
            'closeOnConfirm': false,
            'showLoaderOnConfirm': true,
            'inputPlaceholder': params['placeholder'] ? params['placeholder'] : '',
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : '确定',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : '取消',
        },function (inputValue) {
            if(inputValue === false) return false;
            if(inputValue === ''){
                swal.showInputError('输入框不能为空！');
                return false;
            }
            if(params['confirmCallback']){
                params['confirmCallback'](inputValue);
            }
        });
    },
    'alertInfoToast':function (msg) {
        this.alertToast(msg,'info');
    },
    'alertErrorToast':function (msg) {
        this.alertToast(msg,'error');
    },
    'alertSuccessToast':function (msg) {
        if(!msg){msg = '成功！';}
        this.alertToast(msg,'success');
    },
    'alertToast':function (msg,type) {
        swal({
            'title': msg,
            'text': '',
            'type': type,
            'showCancelButton': false,
            'showConfirmButton': false,
            'timer': 1000,
        });
    },
    'close': function () {
        swal.close();
    }
};