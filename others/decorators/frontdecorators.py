#coding: utf8


from models.cms.accountmodels import CMSUser
from exts import db
import flask
import  settings
from functools import wraps
from utils import xtjson

def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        id = flask.session.get(settings.SESSION_FRONT_USER_ID)
        if id:
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('f_account.login'))

    return wrapper


def json_login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        id = flask.session.get(settings.SESSION_FRONT_USER_ID)
        if id:
            return func(*args, **kwargs)
        else:
            return xtjson.json_unauth_error()

    return wrapper