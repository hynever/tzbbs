#coding: utf8

from forms.base.baseform import BaseForm
import wtforms
from models.front.accountmodels import FrontPermission

class CMSAddPermissionForm(BaseForm):
    name = wtforms.StringField(validators=[wtforms.validators.InputRequired()])

    def validate_name(self,field):
        name = field.data
        permission = FrontPermission.query.filter_by(name=name).first()
        if permission:
            raise wtforms.ValidationError(u'该权限已存在！')
