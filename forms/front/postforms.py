#coding: utf8
import wtforms
from wtforms import validators

from forms.base.baseform import BaseForm
from utils.captcha.xtcaptcha import Captcha


class PostForm(BaseForm):
    title = wtforms.StringField(validators=[validators.Length(min=3,max=100,message=u'标题长度应该处在3到100之间')])
    content = wtforms.StringField(validators=[validators.Length(min=10,max=10000)])
    captcha = wtforms.StringField(validators=[validators.Length(min=4,max=4)])
    board_id = wtforms.IntegerField(validators=[validators.InputRequired()])

    def validate_captcha(self,field):
        captcha = field.data
        if not Captcha.check_captcha(captcha):
            raise wtforms.ValidationError(u'验证码错误')


class CommentForm(BaseForm):
    post_id = wtforms.IntegerField(validators=[validators.InputRequired(message=u'请填入帖子信息！')])
    content = wtforms.StringField(validators=[validators.InputRequired(message=u'请填入帖子内容！')])
    comment_id = wtforms.IntegerField()