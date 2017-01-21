#coding: utf8
import time

import flask
from flask import request

from exts import db
from forms.front.postforms import PostForm,CommentForm
from models.common.postmodels import PostModel,BoardModel,CommentModel,PostStarModel
from utils import xtjson
from models.front.accountmodels import FrontUser,FrontRole,FrontPermission
from enumerations import PostSortType
from others.decorators.frontdecorators import login_required,json_login_required
import settings
from sqlalchemy import and_

bp = flask.Blueprint('post',__name__,url_prefix='/post/')

@bp.route('/',methods=('GET','POST'))
@login_required
def post():
    form = PostForm(request.form)
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.filter_by(id=board_id).first()
            author = flask.g.front_user
            post = PostModel(title=title,content=content,author=author,board=board)
            db.session.add(post)
            db.session.commit()
            if request.is_xhr:
                return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())
    else:
        # 如果积分不够允许发布帖子的最低积分，则跳转到没有权限界面
        if flask.g.front_user.points < settings.POST_ALLOW_POINTS:
            return flask.abort(401)

        context = {
            'boards': BoardModel.query.all()
        }
        return flask.render_template('front/post/add_post.html', **context)


@bp.route('detail/<post_id>',methods=['GET'])
def detail(post_id=0):
    post = PostModel.query.filter_by(id=post_id).first()
    if post and not post.is_removed:
        post.readed_count += 1
        db.session.commit()
        context = {
            'post': post,
            'boards': BoardModel.query.all(),
            'star_authors': [star.author.id for star in post.stars]
        }
        return flask.render_template('front/post/post_detail.html', **context)
    else:
        flask.abort(404)

@bp.route('list/<board>/<sort>/<page>/',methods=['GET'])
def list(board=None,sort=PostSortType.TIME,page=1):
    if not page:
        page = 1
    else:
        page = int(page)

    context = {
        'boards': BoardModel.query.all(),
        'c_board': board,
        'c_sort': sort
    }

    context.update(PostModel.post_list(page,sort_type = sort or PostSortType.TIME,board=board))
    return flask.render_template('front/post/front_index.html', **context)

@bp.route('star/',methods=['POST'])
@json_login_required
def star():
    post_id = flask.request.form.get('post_id')
    if not post_id:
        return xtjson.json_params_error(message=u'您要赞哪个帖子呢？')

    post = PostModel.query.get(post_id)
    star = PostStarModel(post=post,author=flask.g.front_user)
    post.stars.append(star)
    db.session.add(star)
    db.session.commit()
    return xtjson.json_result()

@bp.route('unstar/',methods=['POST'])
@json_login_required
def unstar():
    post_id = flask.request.form.get('post_id')
    if not post_id:
        return xtjson.json_params_error(message=u'您要赞哪个帖子呢？')

    star = PostStarModel.query.filter(and_(PostStarModel.author_id==flask.g.front_user.id,PostStarModel.post_id==post_id)).first()

    if not star:
        return xtjson.json_params_error(message=u'没有该赞数据')

    db.session.delete(star)
    db.session.commit()
    return xtjson.json_result()


@bp.route('comment/',methods=['POST','GET'])
@login_required
def comment():
    if flask.request.method == 'POST':
        form = CommentForm(flask.request.form)
        if form.validate():
            # 先判断该用户是否满足10个积分
            if flask.g.front_user.points < settings.COMMENT_ALLOW_POINTS:
                message = u'您必须达到%s个积分才能评论！' % settings.COMMENT_ALLOW_POINTS
                return xtjson.json_params_error(message=message)

            post_id = form.post_id.data
            content = form.content.data
            comment_id = form.comment_id.data
            author = flask.g.front_user
            post = PostModel.query.filter_by(id=post_id).first()
            comment = CommentModel(content=content, author=author, post=post)
            if comment_id:
                origin_comment = CommentModel.query.filter_by(id=comment_id).first()
                comment.origin_comment = origin_comment

            # 评论一次加comment_up_points个积分
            flask.g.front_user.points += settings.COMMENT_UP_POINTS
            db.session.add(comment)
            db.session.commit()
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=form.get_error())
    else:
        post_id = flask.request.args.get('post_id')
        post = PostModel.query.get(post_id)
        comment_id = flask.request.args.get('comment_id')
        context = {
            'post': post,
        }
        if comment_id:
            comment = CommentModel.query.get(comment_id)
            context['origin_comment'] = comment

        return flask.render_template('front/post/reply.html',**context)


@bp.route('test/')
def test():
    for x in xrange(100):
        title = '美国媒体报道-%s-' % x
        content = """
                        据美国《华尔街日报》12月25日报道，针对谴责以色列在约旦河西岸建造犹太人定居点的联合国安理会决议，美国拒绝投下否决票，以色列总理内塔尼亚胡周日召见了美国大使，对奥巴马政府展开严厉抨击。

            　　报道称，以色列总理内塔尼亚胡在内阁会议上说，毫无疑问，该决议无疑是奥巴马政府发起、支持、协调措辞而且要求通过的。

            　　以色列外交部还召见10个对此决议投支持票国家的大使。

            　　被通过的安理会决议要求以色列“立即和完全停止在包括东耶路撒冷在内的所有巴勒斯坦被占领土上的定居点活动”，这是联合国安理会36年来首次通过决议谴责以色列的定居点建设。共有赞成14个国家投了赞成票，而美国选择了弃权，在此之前美国一直使用否决权阻止这样的对以决议。
            美国国务院发言人证实，内塔尼亚胡与美国驻以色列大使夏皮罗举行了会面，但拒绝对此事发表评论。

            　　报道称，以色列外交部连续两天谴责白宫在联合国涉以决议上的放行姿态，并强调了以色列总理内塔尼亚胡和奥巴马总统在巴以问题上的深刻分歧。

            　　安理会是应委内瑞拉、塞内加尔、新西兰和马来西亚四国的要求进行表决的。这项提案最早由埃及发起，但埃及在埃及总统塞西和美国当选总统特朗普通过电话之后，撤回了要求。

            　　报道称，美国候任总统特朗普星期六重申了他对以色列的支持，称联合国的决议将使和平谈判变得更加困难。

            　　以色列总理内塔尼亚胡也表示期待会见特朗普，“新政府或许会有些新的想法”。【环球网报道 记者余鹏飞】
                    """
        author = FrontUser.query.first()
        # title, content, author
        post = PostModel(title=title, content=content, author=author, board=BoardModel.query.first())
        db.session.add(post)
    db.session.commit()
    return 'success'