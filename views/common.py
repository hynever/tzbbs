#coding: utf8

import flask
from utils.captcha import xtcaptcha
from utils import xtcache
try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
import qiniu
from utils import xtjson
from utils.xtmail import XTMail,XTMailType
import top.api


bp = flask.Blueprint('common',__name__,url_prefix='/common/')

@bp.route('captcha/')
def captcha():
    text,image = xtcaptcha.Captcha.gene_code()

    # 需要通过StringIO这个类来把图片当成流的形式返回给客户端
    out = StringIO() # 获取这个管道
    image.save(out,'png') #将这个图片保存到管道中
    out.seek(0) #移动流指针到第0个位置

    response = flask.make_response(out.read())
    return response

@bp.route('qiniu_token/')
def qiniu_token():

    # 设置AccessKey和SecretKey
    access_key = ''
    secret_key = ''

    # 授权
    q = qiniu.Auth(access_key,secret_key)

    # 选择七牛的云空间
    bucket_name = 'hyvideo'

    # 生成token
    token = q.upload_token(bucket_name)

    # 返回
    return xtjson.json_result(kwargs={'uptoken':token})

@bp.route('email_captcha/')
def email_captcha():
    email = flask.request.args.get('email')

    if not email:
        return xtjson.json_params_error(message=u'请输入邮箱！')

    if xtcache.get(email):
        return xtjson.json_params_error(message=u'该邮箱已经申请验证码！')

    email_captcha = xtcaptcha.Captcha.gene_text()
    xtcache.set(email,email_captcha,timeout=60)

    # 发送邮件
    xtmail = XTMail(mail_type=XTMailType.MAIL_CAPTCHA)
    xtmail.send_mail(email)


    return xtjson.json_result()

@bp.route('telphone_captcha/')
def telphone_captcha():
    telphone = flask.request.args.get('telphone')

    if not telphone:
        return xtjson.json_params_error(message=u'请输入手机号码！')

    if xtcache.get(telphone):
        return xtjson.json_params_error(message=u'该手机号码已经申请过验证码，请在10分钟后再试！')

    telphone_captcha = xtcaptcha.Captcha.gene_text()
    xtcache.set(telphone,telphone_captcha,timeout=600) # 10分钟过期

    app_key = ''
    app_secret = ''
    req = top.setDefaultAppInfo(app_key,app_secret)
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.extend = ""
    req.sms_type = 'normal'
    req.sms_free_sign_name = 'python论坛'
    req.sms_param = "{code:'%s'}" % telphone_captcha
    req.rec_num = telphone.decode('utf-8').encode('ascii')
    req.sms_template_code = 'SMS_37105066'
    try:
        resp = req.getResponse()
        return xtjson.json_result()
    except Exception,e:
        return xtjson.json_params_error(message=u'短信发送太频繁')


