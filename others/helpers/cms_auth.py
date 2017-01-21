#coding: utf8

from models.cms.accountmodels import CMSUser
import flask
from settings import SESSION_CMS_USER_ID
from datetime import datetime

def login_cms(email,password):
    user = CMSUser.query.filter_by(email=email).first()
    if user and user.check_password(password) and user.is_active:
        # 设置session
        flask.session[SESSION_CMS_USER_ID] = user.id
        # 设置上次登录的时间
        user.last_login_time = datetime.now()
        return user
    else:
        return None


def logout_cms():
    try:
        flask.session.pop(SESSION_CMS_USER_ID,None)
        return True
    except Exception:
        return False
