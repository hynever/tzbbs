#coding: utf8

from forms.base.baseform import BaseForm
import wtforms
from models.common.postmodels import PostModel
from models.cms.accountmodels import CMSUser

class CMSHighlightForm(BaseForm):
    post_id = wtforms.IntegerField(validators=[wtforms.validators.InputRequired()])

    def validate_post_id(self,field):
        post_id = field.data
        post = PostModel.query.filter_by(id=post_id).first()
        if not post:
            return wtforms.ValidationError(u'该帖子不存在！')


class CMSAddBoardForm(BaseForm):
    name = wtforms.StringField(validators=[wtforms.validators.Length(min=1,max=20),wtforms.validators.InputRequired()])


class CMSNameForm(BaseForm):
    name = wtforms.StringField(validators=[wtforms.validators.Length(min=1,max=20),wtforms.validators.InputRequired(message=u'名称不能为空！')])


class CMSIdForm(BaseForm):
    id = wtforms.IntegerField(validators=[wtforms.validators.InputRequired(message=u'id不能为空！')])


class CMSIdNameForm(CMSNameForm,CMSIdForm):
    pass

class CMSStringIdForm(BaseForm):
    id = wtforms.StringField(validators=[wtforms.validators.InputRequired(message=u'id不能为空！')])


class CMSAddUserForm(BaseForm):
    username = wtforms.StringField(validators=[wtforms.validators.InputRequired()])
    email = wtforms.StringField(validators=[wtforms.validators.Email(),wtforms.validators.InputRequired()])

    def validate_email(self,field):
        email = field.data
        user = CMSUser.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(u'该邮箱已存在！')


class CMSEditUserForm(CMSAddUserForm,CMSStringIdForm):

    def validate_email(self,field):
        pass
