#coding: utf8

from flask import Flask,render_template,redirect,url_for
from flask_wtf import CsrfProtect
import flask

import config
from exts import db,mail
from views import common
from views.front import postviews,accountviews
from views.cms import cmsviews
from settings import SESSION_CMS_USER_ID
from models.cms.accountmodels import CMSUser
import settings
from models.front.accountmodels import FrontUser
from models.common.postmodels import PostModel,BoardModel

app = Flask(__name__)
app.config.from_object(config)


# 数据库绑定
db.init_app(app)
mail.init_app(app)


# csrf保护
CsrfProtect(app)

# 注册蓝图
app.register_blueprint(common.bp)
app.register_blueprint(postviews.bp)
app.register_blueprint(accountviews.bp)
app.register_blueprint(cmsviews.bp)


@app.route('/')
def index():
    context = {
        'boards': BoardModel.query.all()
    }
    context.update(PostModel.post_list(page=1))
    return render_template('front/post/front_index.html',**context)

@app.errorhandler(401)
def unauth_page(error):
    return render_template('front/post/no_permission.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('common/error/404.html')

@app.after_request
def after_request(response):
    if flask.request.endpoint != 'static':
        return response
    response.cache_control.max_age = 0
    return response

@app.context_processor
def context_processor():
    if hasattr(flask.g, 'front_user'):
        return {'front_user': flask.g.front_user}
    else:
        return {}

@app.before_request
def before_request():
    if not hasattr(flask.g,'front_user'):
        user_id = flask.session.get(settings.SESSION_FRONT_USER_ID)
        user = FrontUser.query.filter_by(id=user_id).first()
        setattr(flask.g,'front_user',user)


@app.template_filter('handle_time')
def handle_time(time):
    from datetime import datetime
    if type(time) == datetime:
        now = datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return u'刚刚'
        elif timestamp > 60 and timestamp < 60*60:
            minutes = timestamp / 60
            return u'%s分钟前' % int(minutes)
        elif timestamp > 60*60 and timestamp < 60*60*24:
            hours = timestamp / (60*60)
            return u'%s小时前' % int(hours)
        elif timestamp > 60*60*24 and timestamp < 60*60*24*30:
            days = timestamp / (60*60*24)
            return u'%s天前' % int(days)
        elif now.year == time.year:
            return time.strftime('%m-%d %H:%M:%S')
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S')
    return time


if __name__ == '__main__':
    app.run(port=8000)
