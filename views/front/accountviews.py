#coding: utf8
import flask
from exts import db
from forms.front.accountforms import RegistForm,LoginForm,SettingsForm
from models.front.accountmodels import FrontUser,FrontRole
from others.helpers.front_auth import login_front,logout_front
from others.decorators.frontdecorators import login_required
from utils import  xtjson
from models.common.postmodels import PostModel,CommentModel

bp = flask.Blueprint('f_account',__name__,url_prefix='/account/')

@bp.route('login/',methods=['POST','GET'])
def login():
    if flask.request.method == 'POST':
        form = LoginForm(flask.request.form)
        if form.validate():
            telphone = form.telphone.data
            password = form.password.data
            user = login_front(telphone,password)
            if user:
                remember = form.remember.data
                if remember:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                return flask.redirect(flask.url_for('index'))
            else:
                return flask.render_template('front/account/front_login.html',message=u'手机号或密码错误！')
        else:
            return flask.render_template('front/account/front_login.html',message=form.get_error())
    else:
        return flask.render_template('front/account/front_login.html')

@bp.route('logout/',methods=['GET'])
@login_required
def logout():
    logout_front()
    return flask.redirect(flask.url_for('index'))


@bp.route('regist/',methods=['POST','GET'])
def regist():
    if flask.request.method == 'POST':
        form = RegistForm(flask.request.form)
        if form.validate():
            telphone = form.telphone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(username=username,telphone=telphone,password=password)
            db.session.add(user)
            db.session.commit()
            login_front(telphone,password)
            return flask.redirect(flask.url_for('index'))
        else:
            context = {
                "message":form.get_error(),
                'username': form.username.data,
                'password': form.password.data,
                'confirm_password': form.confirm_password.data,
                'telphone': form.telphone.data,
                'telphone_captcha': form.telphone_captcha.data
            }
            return flask.render_template('front/account/front_regist.html',**context)
    else:
        return flask.render_template('front/account/front_regist.html')


@bp.route('settings/',methods=['POST','GET'])
@login_required
def settings():
    if flask.request.method == 'POST':
        form = SettingsForm(flask.request.form)
        if form.validate():
            id = form.id.data
            username = form.username.data
            realname = form.realname.data
            qq = form.qq.data
            avatar = form.avatar.data
            signature = form.signature.data
            user = FrontUser.query.get(id)
            if user:
                if username and len(username) > 0:
                    user.username = username
                if realname and len(realname) > 0:
                    user.realname = realname
                if qq and len(qq) > 0:
                    user.qq = qq
                if avatar and len(avatar) > 0:
                    user.avatar = avatar
                if signature and len(signature) > 0:
                    user.signature = signature

                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'该用户不存在！')
        else:
            return xtjson.json_params_error(message=form.get_error())
    else:
        return flask.render_template('front/account/front_settings.html')


@bp.route('profile/<user_id>',methods=['GET'])
def profile(user_id=0):
    if not user_id:
        return flask.abort(404)

    user = FrontUser.query.get(user_id)
    if user:
        context = {
            'current_user': user
        }
        return flask.render_template('front/account/front_profile.html',**context)
    else:
        return flask.abort(404)

@bp.route('profile/posts/',methods=['GET'])
def profile_posts():
    user_id = flask.request.args.get('user_id')
    if not user_id:
        return flask.abort(404)

    user = FrontUser.query.get(user_id)
    print '-' * 20
    print len(user.posts)
    print '-' * 20
    if user:
        context = {
            'current_user': user,
        }
        return flask.render_template('front/account/front_profile_posts.html',**context)
    else:
        return flask.abort(404)

@bp.route('create_user/',methods=['GET'])
def create_user():
    username = 'xiaotuo'
    password = '111111'
    telphone = '15579986326'
    user = FrontUser(username=username,telphone=telphone,password=password)
    db.session.add(user)
    db.session.commit()
    return 'success'


