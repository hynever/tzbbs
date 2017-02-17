#coding: utf8

import flask
from others.decorators.cmsdecorators import login_required,superadmin_required
from flask import render_template
from forms.cms.accountforms import CMSLoginForm,CMSResetpwdForm,CMSResetemailForm
from models.front.accountmodels import FrontRole
from forms.cms.postforms import CMSHighlightForm,CMSAddBoardForm,CMSNameForm,CMSIdNameForm,CMSIdForm,CMSStringIdForm,CMSAddUserForm,CMSEditUserForm
from models.cms.accountmodels import CMSUser,CMSRole,CMSPermission
from models.common.postmodels import PostModel,BoardModel,HighlightPostModel,CommentModel
from models.front.accountmodels import FrontUser
from others.helpers import cms_auth
from settings import SESSION_CMS_USER_ID
from exts import db
from utils import xtjson
import settings
from enumerations import PostSortType


bp = flask.Blueprint('cms',__name__,url_prefix='/cms/')


@bp.route('/')
@login_required
def home():
    return flask.render_template('cms/base/cms_home.html')


@bp.route('profile/')
@login_required
def profile():
    return flask.render_template('cms/account/cms_profile.html')

@bp.route('resetpwd/',methods=['GET','POST'])
@login_required
def resetpwd():
    message = None
    if flask.request.method == 'POST':
        form = CMSResetpwdForm(flask.request.form)
        if form.validate():
            newpwd = form.newpwd1.data
            user = flask.g.cms_user
            user.password = newpwd
            db.session.commit()
            return xtjson.json_result()
        else:
            message = form.get_error()
            return xtjson.json_params_error(message=message)
    else:
        return flask.render_template('cms/account/cms_resetpwd.html')


@bp.route('resetemail/',methods=['GET','POST'])
@login_required
def resetemail():
    message = None
    if flask.request.method == 'POST':
        form = CMSResetemailForm(flask.request.form)
        if form.validate():
            email = form.email.data
            user = flask.g.cms_user

            if user.email == email:
                return xtjson.json_params_error(u'邮箱未修改！')

            user.email = email
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())
    else:
        return render_template('cms/account/cms_resetemail.html')


@bp.route('login/',methods=['GET','POST'])
def login():
    message = None
    # 如果已经登录，直接跳转到首页
    if flask.g.is_login:
        return flask.redirect(flask.url_for('cms.home'))

    if flask.request.method == 'POST':
        form = CMSLoginForm(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            # 登录
            user = cms_auth.login_cms(email,password)
            if user:
                # 记住我
                remember = form.remember.data
                if remember:
                    # 如果设置为True，
                    # 则会过期时间为session.permanent_session_lifetime
                    # 这个值默认为30天
                    flask.session.permanent = True
                else:
                    # 如果为False，则浏览器关闭后就过期
                    flask.session.permanent = False
                return flask.redirect(flask.url_for('cms.home'))
            else:
                message = u'邮箱或密码错误！'
        else:
            message = form.get_error()

    return flask.render_template('cms/account/cms_login.html',message=message)


@bp.route('logout/',methods=['GET'])
@login_required
def logout():
    cms_auth.logout_cms()
    return flask.redirect(flask.url_for('cms.login'))


@bp.route('posts/')
@login_required
def posts():
    page = flask.request.args.get('page')
    sort = flask.request.args.get('sort')
    board = flask.request.args.get('board')

    if not page:
        page = 1    #默认为1
    else:
        page = int(page)

    if not sort:
        # 1 代表的是按时间倒序排序
        sort = PostSortType.TIME
    else:
        sort = int(sort)

    #  获取所有的板块
    boards = BoardModel.query.all()

    context = {
        'boards': boards,
    }
    context.update(PostModel.post_list(page,sort_type=sort,board=board))
    return render_template('cms/post/cms_posts.html',**context)


@bp.route('highlight/',methods=['POST'])
@login_required
def highlight():
    form = CMSHighlightForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        post = PostModel.query.filter_by(id=post_id).first()
        highlight = HighlightPostModel()
        post.highlight = highlight
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('unhighlight/',methods=['POST'])
@login_required
def unhighlight():
    form = CMSHighlightForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        post = PostModel.query.filter_by(id=post_id).first()
        highlight = post.highlight
        post.highlight = None
        db.session.delete(highlight)
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

##########评论相关start##########
@bp.route('comments/',methods=['GET'])
@login_required
def comments():
    page = flask.request.args.get('page')
    if not page:
        page = 1
    context = CommentModel.comment_list(int(page))
    return flask.render_template('cms/post/cms_comments.html', **context)

@bp.route('comments/remove_comment/',methods=['POST'])
@login_required
def remove_comment():
    form = CMSIdForm(flask.request.form)
    if form.validate():
        id = form.id.data
        comment = CommentModel.query.get(id)
        comment.is_removed = True
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())
##########评论相关end##########


@bp.route('remove/',methods=['POST'])
@login_required
def remove():
    form = CMSHighlightForm(flask.request.form)
    if form.validate():
        post_id = form.post_id.data
        post = PostModel.query.filter_by(id=post_id).first()
        post.is_removed = True
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('boards/add_board/',methods=('POST','GET'))
@login_required
def add_board():
    if flask.request.method == 'POST':
        form = CMSNameForm(flask.request.form)
        if form.validate():
            try:
                name = form.name.data
                board = BoardModel(name=name,author=flask.g.cms_user)
                db.session.add(board)
                db.session.commit()
                return xtjson.json_result(data=board.to_dict())
            except Exception,e:
                return xtjson.json_server_error()
        else:
            print form.get_error()
            return xtjson.json_params_error(message=form.get_error())
    else:
        context = {
            'roles': FrontRole.query.all(),
        }
        return render_template('cms/post/cms_add_board.html',**context)


@bp.route('boards/edit_board/',methods=['POST'])
@login_required
def edit_board():
    form = CMSIdNameForm(flask.request.form)
    if form.validate():
        name = form.name.data
        id = form.id.data
        board = BoardModel.query.get(id)
        board.name = name
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())


@bp.route('delete_board/',methods=['POST'])
@login_required
def delete_board():
    form = CMSIdForm(flask.request.form)
    if form.validate():
        id = form.id.data
        board = BoardModel.query.filter_by(id=id).first()
        if len(board.posts) > 0:
            return xtjson.json_params_error(message=u'该板块下有帖子，不能删除！')
        else:
            db.session.delete(board)
            db.session.commit()
            return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('boards/',methods=['GET','POST'])
@login_required
def boards():
    if flask.request.method == 'POST':
        pass
    else:
        # 查找所有的板块
        boards = BoardModel.query.all()
        context = {
            'boards': boards
        }
        return render_template('cms/post/cms_boards.html',**context)


@bp.route('roles/',methods=['GET','POST'])
@login_required
def roles():
    context = {
        'roles': FrontRole.query.all()
    }
    return render_template('cms/post/cms_roles.html',**context)


@bp.route('add_role/',methods=['POST'])
@login_required
def add_role():
    name = flask.request.form.get('name')
    if name:
        role = FrontRole(name=name,author=flask.g.cms_user)
        db.session.add(role)
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=u'请输入分组名称！')

@bp.route('edit_role/',methods=['POST'])
@login_required
def edit_role():
    name = flask.request.form.get('name')
    if name:
        form = CMSIdNameForm(flask.request.form)
        if form.validate():
            name = form.name.data
            id = form.id.data
            role = FrontRole.query.filter_by(id=id).first()
            role.name = name
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())
    return xtjson.json_method_error(message=u'请输入分组名称！')

@bp.route('delete_role/',methods=['POST'])
@login_required
def delete_role():
    form = CMSIdForm(flask.request.form)
    if form.validate():
        id = form.id.data
        role = FrontRole.query.filter_by(id=id).first()
        if len(role.users) > 0:
            return xtjson.json_params_error(message=u'这个分组下尚存在用户，不能删除！')
        else:
            db.session.delete(role)
            db.session.commit()
            return xtjson.json_result()
    else:
        message = form.get_error()
        return xtjson.json_params_error(message=message)



##########用户相关start##########
@bp.route('users/',methods=['GET'])
@login_required
def users():
    context = {
        'users': FrontUser.query.all()
    }
    return render_template('cms/post/cms_users.html',**context)

@bp.route('users/edit_user/',methods=['GET','POST'])
@login_required
def edit_user():
    if flask.request.method == 'POST':
        form = CMSStringIdForm(flask.request.form)
        if form.validate():
            id = form.id.data
            roles = flask.request.form.getlist('roles[]')
            user = FrontUser.query.get(id)
            if user.roles:
                user.roles.clear()
            if roles and len(roles) > 0:
                for role_id in roles:
                    role = FrontRole.query.get(role_id)
                    if role:
                        user.roles.append(role)

            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())
    else:
        user_id = flask.request.args.get('id')
        user = FrontUser.query.get(user_id)
        context = {
            'roles': FrontRole.query.all(),
            'user': user,
            'current_roles': [role.id for role in user.roles]
        }
        return render_template('cms/post/cms_edit_user.html',**context)


@bp.route('users/add_backlist/',methods=['POST'])
@login_required
def add_backlist():
    form = CMSStringIdForm(flask.request.form)
    if form.validate():
        id = form.id.data
        user = FrontUser.query.filter_by(id=id).first()
        user.is_active = False
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('users/remove_backlist/',methods=['POST'])
@login_required
def remove_backlist():
    form = CMSStringIdForm(flask.request.form)
    if form.validate():
        id = form.id.data
        user = FrontUser.query.filter_by(id=id).first()
        user.is_active = True
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())
##########用户相关end##########


##########cms用户相关start##########
@bp.route('cmsuser_manage/',methods=['GET'])
@login_required
def cmsuser_manage():
    context = {
        'cms_users': CMSUser.query.all()
    }
    return render_template('cms/supermanage/cms_cmsusers.html',**context)

@bp.route('cmsuser_manage/add_cmsuser/',methods=['GET','POST'])
@login_required
def add_cmsuser():
    if flask.request.method == 'POST':
        form = CMSAddUserForm(flask.request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            roles = flask.request.form.getlist('roles[]')
            user = CMSUser(username=username,email=email,password='111111')
            if roles:
                for role_id in roles:
                    role = CMSRole.query.filter_by(id=role_id).first()
                    user.roles.append(role)
                db.session.add(user)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'请最少选择一种分组！')
        else:
            return xtjson.json_result(message=form.get_error())
    else:
        context = {
            'roles': CMSRole.query.all(),
        }
        return render_template('cms/supermanage/cms_addcmsuser.html',**context)

@bp.route('cmsuser_manage/edit_cmsuser/', methods=['GET', 'POST'])
@login_required
def edit_cmsuser():
    if flask.request.method == 'POST':
        form = CMSEditUserForm(flask.request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            user_id = form.id.data
            user = CMSUser.query.get(user_id)
            user.username = username
            user.email = email
            roles = flask.request.form.getlist('roles[]')
            if roles and len(roles) > 0:
                print '-'*30
                print 'coming...'
                print '-'*30
                user.roles[:] = []
                for role_id in roles:
                    role = CMSRole.query.filter_by(id=role_id).first()
                    user.roles.append(role)
                db.session.add(user)
                db.session.commit()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'请最少选择一种分组！')
        else:
            return xtjson.json_params_error(message=form.get_error())
    else:
        user_id = flask.request.args.get('user_id')
        user = CMSUser.query.get(user_id)
        current_roles = [role.id for role in user.roles]
        context = {
            'roles': CMSRole.query.all(),
            'user': user,
            'current_roles': current_roles
        }
        return render_template('cms/supermanage/cms_editcmsuser.html', **context)


@bp.route('cmsuser_manage/add_cmsuser_backlist/',methods=['POST'])
@login_required
@superadmin_required
def add_cmsuser_backlist():
    form = CMSStringIdForm(flask.request.form)
    if form.validate():
        id = form.id.data
        user = CMSUser.query.get(id)
        print 'coming....'
        user.is_active = False
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('cmsuser_manage/remove_cmsuser_backlist/', methods=['POST'])
@login_required
@superadmin_required
def remove_cmsuser_backlist():
    form = CMSStringIdForm(flask.request.form)
    if form.validate():
        id = form.id.data
        user = CMSUser.query.get(id)
        user.is_active = True
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())
##########cms用户相关end##########


##########cms分组相关start##########
@bp.route('cmsrole_manage/',methods=['GET'])
@login_required
@superadmin_required
def cmsrole_manage():
    context = {
        'cms_roles': CMSRole.query.all()
    }
    return render_template('cms/supermanage/cms_cmsroles.html',**context)

@bp.route('cmsrole_manage/add_cmsrole/',methods=['POST'])
@login_required
@superadmin_required
def add_cmsrole():
    form = CMSNameForm(flask.request.form)
    if form.validate():
        name = form.name.data
        role = CMSRole(name=name)
        db.session.add(role)
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('cmsrole_manage/delete_cmsrole/',methods=['POST'])
@login_required
@superadmin_required
def delete_cmsrole():
    form = CMSIdForm(flask.request.form)
    if form.validate():
        id = form.id.data
        role = CMSRole.query.filter_by(id=id).first()
        if len(role.users) > 0:
            return xtjson.json_params_error(message=u'该组下还存在用户，不能删除！')
        db.session.delete(role)
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())

@bp.route('cmsrole_manage/edit_cmsrole/',methods=['POST'])
@login_required
@superadmin_required
def edit_cmsrole():
    form = CMSIdNameForm(flask.request.form)
    if form.validate():
        id = form.id.data
        name = form.name.data
        role = CMSRole.query.filter_by(id=id).first()
        role.name = name
        db.session.commit()
        return xtjson.json_result()
    else:
        return xtjson.json_params_error(message=form.get_error())
##########cms分组相关end##########


@bp.before_request
def before_request():
    user_id = flask.session.get(SESSION_CMS_USER_ID)
    flask.g.is_login = False
    if user_id:
        user = CMSUser.query.filter_by(id=user_id).first()
        if user:
            flask.g.is_login = True
            flask.g.cms_user = user


@bp.context_processor
def template_extras():
    if hasattr(flask.g,'cms_user'):
        return {'cms_user':flask.g.cms_user}
    return {}