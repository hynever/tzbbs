#coding: utf8

from models.common.basemodels import BaseModel
from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
from datetime import datetime
from models.cms.accountmodels import CMSUser
from operator import or_


# 权限表（不存储数据库的）
class FrontPermission(object):
    PUBLIC = 0x01
    VIP = 0x02

    PERMISSION_MAP = {
        PUBLIC: ('public','公共用户'),
        VIP: ('vip','VIP学生')
    }


# 用户-角色多对多的关系表
user_role = db.Table('front_user_role',
        db.Column('user_id',db.String(30),db.ForeignKey('front_user.id')),
        db.Column('role_id',db.Integer,db.ForeignKey('front_role.id')))

# 前台用户表
class FrontUser(db.Model,BaseModel):
    __tablename__ = 'front_user'

    id = db.Column(db.String(30),primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    telphone = db.Column(db.String(20),nullable=False,unique=True)
    email = db.Column(db.String(100),unique=True)
    _password = db.Column(db.String(200),nullable=False)
    joined_time = db.Column(db.DateTime,default=datetime.now())
    gender = db.Column(db.SMALLINT,default=0)
    points = db.Column(db.Integer,default=0) # 积分
    avatar = db.Column(db.String(200),nullable=True)
    realname = db.Column(db.String(50),nullable=True)
    qq = db.Column(db.String(20),nullable=True)
    signature = db.Column(db.String(200))
    is_active = db.Column(db.Boolean,default=True)
    github_url = db.Column(db.String(200))  # github地址
    homepage = db.Column(db.String(200))    #个人主页
    last_login_time = db.Column(db.DateTime,nullable=True)

    roles = db.relationship('FrontRole',secondary=user_role)

    def __init__(self,username,telphone,password):
        self.id = shortuuid.uuid()
        self.username = username
        self.telphone = telphone
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def has_permission(self,permission):
        if self.roles is None or len(self.roles) ==0:
            return False
        all_permissions = reduce(or_,map(lambda x: x.permissions,self.roles))
        return all_permissions & permission == permission

    @property
    def is_vip(self):
        return self.has_permission(FrontPermission.VIP)

    @property
    def permissions(self):
        if self.roles is None:
            return None
        permissions = reduce(or_,map(lambda x: x.permissions,self.roles))
        permission_dicts = []
        for key,value in FrontPermission.PERMISSION_MAP.items():
            if key & permissions:
                permission_dicts.append({key:value})
        return permission_dicts

    @property
    def boards(self):
        board_ids = []
        boards = []
        for role in self.roles:
            for board in role.boards:
                if board.id not in board_ids:
                    board_ids.append(board.id)
                    boards.append(board)
        return boards


# 角色表
class FrontRole(db.Model,BaseModel):
    __tablename__ = 'front_role'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    create_time = db.Column(db.DateTime,default=datetime.now())
    permissions = db.Column(db.Integer,default=FrontPermission.PUBLIC)
    author_id = db.Column(db.String(30),db.ForeignKey('cms_user.id'))

    author = db.relationship('CMSUser',backref='front_roles')

    users = db.relationship('FrontUser',secondary=user_role)

    def __init__(self, name,author):
        self.name = name
        self.author = author




