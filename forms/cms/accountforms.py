#coding: utf8
from forms.base.baseform import BaseForm
import wtforms
from utils.captcha import xtcaptcha
import flask
from models.cms.accountmodels import CMSUser

class CMSLoginForm(BaseForm):
    email = wtforms.StringField(validators=[wtforms.validators.email(),wtforms.validators.InputRequired(message=u'请填写邮箱！')])
    password = wtforms.StringField(validators=[wtforms.validators.InputRequired(message=u'请填写密码！')])
    # captcha = wtforms.StringField(validators=[wtforms.validators.Length(min=4,max=4)])
    remember = wtforms.BooleanField()

    # def validate_captcha(self,field):
    #     if not xtcaptcha.Captcha.check_captcha(field.data):
    #         raise wtforms.ValidationError(u'验证码错误！')


class CMSResetpwdForm(BaseForm):
    oldpwd = wtforms.StringField(validators=[wtforms.validators.InputRequired(message=u'请输入原始密码！')])
    newpwd1 = wtforms.StringField(validators=[wtforms.validators.InputRequired(message=u'请输入新密码！'),wtforms.validators.Length(min=4,max=20),wtforms.validators.EqualTo('newpwd2',message=u'两次密码不相等！')])
    newpwd2 = wtforms.StringField(validators=[wtforms.validators.InputRequired(message=u'请输入新密码！'),wtforms.validators.Length(min=4,max=20)])

    def validate_oldpwd(self,field):
        if flask.g.is_login:
            user = flask.g.cms_user
            if not user.check_password(field.data):
                raise wtforms.ValidationError(u'原始密码错误！')


class CMSResetemailForm(BaseForm):
    email = wtforms.StringField(validators=[wtforms.validators.InputRequired(message=u'请输入邮箱！'),wtforms.validators.email()])
    captcha = wtforms.StringField(validators=[wtforms.validators.InputRequired(message=u'请输入验证码！')])

    def validate_captcha(self,field):
        captcha = field.data
        if not xtcaptcha.Captcha.check_captcha(captcha):
            return wtforms.ValidationError(u'验证码错误！')


    def validate_email(self,field):
        email = field.data
        user = CMSUser.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(u'该邮箱已经被使用！')