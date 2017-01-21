#coding: utf8

from models.cms.accountmodels import CMSUser
from exts import db
import flask
import  settings
from functools import wraps

def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        id = flask.session.get(settings.SESSION_CMS_USER_ID)
        if id:
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('cms.login'))

    return wrapper



def superadmin_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        user = flask.g.cms_user
        if user.is_superadmin:
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('cms.home'))

    return wrapper
