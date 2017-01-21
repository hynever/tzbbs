#coding: utf8
from datetime import datetime
from exts import db
from basemodels import BaseModel
import settings
from models.front.accountmodels import FrontUser
from enumerations import PostSortType
from models.cms.accountmodels import CMSUser
from sqlalchemy import or_,and_
from sqlalchemy import func


front_role_board = db.Table('front_role_board',
                db.Column('board_id',db.Integer,db.ForeignKey('boardmodel.id')),
                db.Column('role_id',db.Integer,db.ForeignKey('front_role.id')))

# 板块模型
class BoardModel(db.Model,BaseModel):
    __tablename__ = 'boardmodel'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    create_time = db.Column(db.DateTime,default=datetime.now())
    is_public = db.Column(db.Boolean,default=False)
    author_id = db.Column(db.String(30),db.ForeignKey('cms_user.id'))

    author = db.relationship('CMSUser',backref='boards')
    roles = db.relationship('FrontRole',secondary=front_role_board,backref='boards')

    def __init__(self,name,author,public=True):
        self.name = name
        self.author = author
        self.is_public = public


class CommentModel(db.Model,BaseModel):
    __tablename__ = 'commentmodel'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now())
    is_removed = db.Column(db.Boolean,default=False)
    author_id = db.Column(db.String(30),db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('postmodel.id'))
    origin_comment_id = db.Column(db.Integer,db.ForeignKey('commentmodel.id'))

    author = db.relationship('FrontUser',backref=db.backref('comments',lazy='dynamic'))
    post = db.relationship('PostModel',backref=db.backref('comments',order_by=id.desc()))
    origin_comment = db.relationship('CommentModel',backref='replys',remote_side=[id])


    def __init__(self,content,author,post,origin_comment=None):
        self.content = content
        self.author = author
        self.post = post
        self.origin_comment = origin_comment

    @classmethod
    def comment_list(cls,page):
        start = (page-1)*settings.PAGE_NUM
        end = start + settings.PAGE_NUM

        # 所有的评论
        all_comments = cls.query.filter_by(is_removed=False)
        # 评论的数量
        comments_count = all_comments.count()
        # 切片后的评论
        comments = all_comments[start:end]
        # 页数
        page_count = comments_count / settings.PAGE_NUM
        if page_count > 0 and comments_count % page_count > 0:
            page_count += 1

        pages = []

        # 先往前面找
        tmp_page = page - 1
        while tmp_page >= 1:
            if tmp_page % 5 == 0:
                break
            else:
                pages.append(tmp_page)
                tmp_page -= 1

        # 往后面找
        tmp_page = page
        while tmp_page <= page_count:
            if tmp_page % 5 == 0:
                pages.append(tmp_page)
                break
            else:
                pages.append(tmp_page)
                tmp_page += 1

        pages.sort()

        return {
            'pages': pages,
            't_page': page_count,
            'c_page': page,
            'comments': comments,
        }


# 加精帖子模型
class HighlightPostModel(db.Model,BaseModel):
    __tablename__ = 'highlight_postmodel'
    id = db.Column(db.Integer,primary_key=True)
    create_time = db.Column(db.DateTime,default=datetime.now())

# 帖子模型
class PostModel(db.Model,BaseModel):
    __tablename__ = 'postmodel'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime,default=datetime.now)
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    readed_count = db.Column(db.Integer,default=0)
    is_removed = db.Column(db.Boolean,default=False)
    highlight_id = db.Column(db.Integer,db.ForeignKey('highlight_postmodel.id'))
    author_id = db.Column(db.String(30),db.ForeignKey('front_user.id'))
    board_id = db.Column(db.Integer,db.ForeignKey('boardmodel.id'))

    board = db.relationship('BoardModel',backref='posts')
    author = db.relationship('FrontUser',backref='posts')
    highlight = db.relationship('HighlightPostModel',backref='post')

    def __init__(self,title,content,author,board):
        self.title = title
        self.content = content
        self.author = author
        self.board = board

    @classmethod
    def post_list(cls,page,board=None,page_num=settings.PAGE_NUM,sort_type=PostSortType.TIME):
        start = (page-1) * page_num
        end = start + page_num

        # 所有的帖子
        all_posts = None

        sort_type = int(sort_type)

        # 按加精排序（没有加精的不会出现）
        if sort_type == PostSortType.HIGHLIGHT:
            all_posts = db.session.query(PostModel).join(HighlightPostModel).filter(PostModel.is_removed==False).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())

        # 按阅读量排序（3）
        elif sort_type == PostSortType.READEDCOUNT:
            all_posts = cls.query.filter_by(is_removed=False).order_by(cls.readed_count.desc(),cls.create_time.desc())


        # 按赞数最多
        elif sort_type == PostSortType.STAR_COUNT:
            stmt = db.session.query(PostStarModel.post_id,func.count(PostStarModel.post_id).label('post_count')).group_by(PostStarModel.post_id).subquery()
            all_posts = db.session.query(PostModel).outerjoin(stmt,PostModel.id==stmt.c.post_id).filter(PostModel.is_removed==False).order_by(stmt.c.post_count.desc())


        # 按时间排序（1）
        elif sort_type == PostSortType.TIME:
            all_posts = cls.query.filter_by(is_removed=False).order_by(cls.create_time.desc())

        # 按评论最多排序
        else:
            stmt = db.session.query(CommentModel.post_id,func.count(CommentModel.post_id).label('post_count')).group_by(CommentModel.post_id).subquery()
            all_posts = db.session.query(PostModel).outerjoin(stmt,PostModel.id==stmt.c.post_id).filter(PostModel.is_removed==False).order_by(stmt.c.post_count.desc())


        # 如果有板块过滤，则进行过滤
        if board and int(board) > 0:
            all_posts = all_posts.filter(PostModel.board_id==board)

        # 总的帖子数量
        post_count = all_posts.count()

        # 切片后的帖子
        posts = all_posts[start:end]

        page_count = post_count / page_num

        if page_count > 0 and post_count % page_count > 0:
            page_count += 1

        pages = []

        # 先往前面找
        tmp_page = page - 1
        while tmp_page >= 1:
            if tmp_page % 5 == 0:
                break
            else:
                pages.append(tmp_page)
                tmp_page -= 1

        # 往后面找
        tmp_page = page
        while tmp_page <= page_count:
            if tmp_page % 5 == 0:
                pages.append(tmp_page)
                break
            else:
                pages.append(tmp_page)
                tmp_page += 1

        pages.sort()

        return {
            'pages': pages,
            't_page': page_count,
            'c_page': page,
            'posts': posts,
            'c_sort': sort_type,
            'c_board': board or 0
        }

class PostStarModel(db.Model,BaseModel):
    __tablename__ = 'post_star'
    id = db.Column(db.Integer,primary_key=True)
    create_time = db.Column(db.DateTime,default=datetime.now())
    post_id = db.Column(db.Integer,db.ForeignKey('postmodel.id'),nullable=False)
    author_id = db.Column(db.String(30),db.ForeignKey('front_user.id'),nullable=False)

    author = db.relationship('FrontUser',backref='stars')
    post = db.relationship('PostModel',backref='stars')


    def __init__(self,author,post):
        self.author = author
        self.post = post