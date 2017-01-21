/**
 * Created by Administrator on 2016/12/20.
 */

var setParams = function (key,value) {
    var href = window.location.href;
    // 重新加载整个页面
    var isReplaced = false;
    var urlArray = href.split('?');
    if(urlArray.length > 1){
        var queryArray = urlArray[1].split('&');
        for(var i=0; i < queryArray.length; i++){
            var paramsArray = queryArray[i].split('=');
            if(paramsArray[0] == key){
                paramsArray[1] = value;
                queryArray[i] = paramsArray.join('=');
                isReplaced = true;
                break;
            }
        }

        if(!isReplaced){
            var params = {};
            params[key] = value;
            if(urlArray.length > 1){
                href = href + '&' + $.param(params);
            }else{
                href = href + '?' + $.param(params);
            }
        }else{
            var params = queryArray.join('&');
            urlArray[1] = params;
            href = urlArray.join('?');
        }
    }else{
        var param = {};
        param[key] = value;
        if(urlArray.length > 1){
            href = href + '&' + $.param(param);
        }else{
            href = href + '?' + $.param(param);
        }
    }
    return href;
}


$(function () {
   $('#sort-select').change(function (event) {
       // 获取当前的值
       var sortValue = $(this).val();
       // 重新加载整个页面
       var href = setParams('sort',sortValue);
       window.location = setParams('sort',sortValue);
       // console.log('sort-href:',href);
   });
});

$(function () {
    $('#filter-select').change(function (event) {
        // 获取当前的值
        var filterValue = $(this).val();
        console.log('value:',filterValue);
        var href = setParams('board',filterValue);
        window.location = href;
        // console.log('href:'+href);
    });
});


$(function () {
    // 加精
    var btns = $('.highlight-btn');
    btns.click(function (event) {
        var self = $(this);
        event.preventDefault();
        // 发送ajax
        xtajax.post({
            'url': '/cms/highlight/',
            'data': {
                'post_id': $(this).attr('data-post-id')
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    // 重新加载整个页面
                    xtalert.alertSuccessToast('加精成功！');
                    setTimeout(function () {
                        window.location = window.location.href;
                    },1000);
                } else {
                    xtalert.alertInfoToast(data['message']);
                }
            },
            'error': function (error) {
                xtalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    // 取消精
    var btns = $('.unhighlight-btn');
    btns.click(function (event) {
        var self = $(this);
        event.preventDefault();
        // 发送ajax
        xtajax.post({
            'url': '/cms/unhighlight/',
            'data': {
                'post_id': self.attr('data-post-id')
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    // 重新加载整个页面
                    xtalert.alertSuccessToast('取消精品成功！');
                    setTimeout(function () {
                        window.location = window.location.href;
                    },1000);
                } else {
                    xtalert.alertInfoToast(data['message']);
                }
            },
            'error': function (error) {
                xtalert.alertNetworkError();
            }
        });
    });
});

$(function () {
    var btns = $('.remove-btn');
    btns.click(function (event) {
        var self = $(this);
        event.preventDefault();
        xtalert.alertConfirm({
            'msg': '您确定要移除这篇帖子吗？',
            'confirmCallback': function () {
                xtajax.post({
                    'url': '/cms/remove/',
                    'data': {
                        'post_id': self.attr('data-post-id')
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            // 重新加载整个页面
                            setTimeout(function () {
                                xtalert.alertSuccessToast('删除成功！');
                            },500);
                            setTimeout(function () {
                                window.location = window.location.href;
                            },1500);
                        } else {
                            xtalert.alertInfoToast(data['message']);
                        }
                    },
                    'error': function (error) {
                        xtalert.alertNetworkError();
                    }
                });
            },
            'cancelCallback': function () {
                // did nothing
            }
        });
    });
});

