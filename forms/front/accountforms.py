#coding: utf8

from forms.base.baseform import BaseForm
import wtforms
from wtforms import validators
from utils.captcha.xtcaptcha import Captcha
from utils import xtcache

class LoginForm(BaseForm):
    telphone = wtforms.StringField(validators=[validators.InputRequired(message=u'请输入手机号码！')])
    password = wtforms.StringField(validators=[validators.InputRequired(message=u'请输入密码！')])
    captcha = wtforms.StringField(validators=[validators.InputRequired(message=u'请输入验证码！')])
    remember = wtforms.BooleanField()

    def validate_captcha(self,field):
        captcha = field.data
        if not Captcha.check_captcha(captcha):
            wtforms.ValidationError(u'验证码错误！')


class RegistForm(BaseForm):
    telphone = wtforms.StringField(validators=[wtforms.validators.InputRequired(message=u'请输入手机号码')])
    telphone_captcha = wtforms.StringField(validators=[wtforms.validators.Length(min=4,max=4),wtforms.validators.InputRequired(message=u'请输入邮箱验证码')])
    username = wtforms.StringField(validators=[wtforms.validators.Length(min=4,max=20,message=u'用户名长度必须处在4-20之间')])
    password = wtforms.StringField(validators=[wtforms.validators.Length(min=6,max=20),wtforms.validators.EqualTo('confirm_password',message=u'两个密码不一致'),wtforms.validators.InputRequired(message=u'请输入密码')])
    confirm_password =  wtforms.StringField()
    graph_captcha = wtforms.StringField(validators=[wtforms.validators.Length(min=4,max=4),wtforms.validators.InputRequired(message=u'请输入图形验证码')])

    def validate_telphone_captcha(self,field):
        telphone_captcha = field.data
        telphone = self.telphone.data
        captcha = xtcache.get(telphone)
        if not captcha or captcha.lower() != telphone_captcha.lower():
            raise wtforms.ValidationError(u'短信验证码错误')


    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        if not Captcha.check_captcha(graph_captcha):
            raise wtforms.ValidationError(u'图形验证码错误')


class SettingsForm(BaseForm):
    id = wtforms.StringField(validators=[validators.InputRequired(u'找不到该用户！')])
    username = wtforms.StringField(validators=[validators.InputRequired(message=u'请输入用户名'),validators.Length(min=2,max=20)])
    realname = wtforms.StringField()
    qq = wtforms.StringField()
    avatar = wtforms.StringField()
    signature = wtforms.StringField()
