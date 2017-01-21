#coding: utf8

from exts import db
from models.common.basemodels import BaseModel
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid
from datetime import datetime
from operator import or_


# CMS权限表
class CMSPermission(object):
    OPERATOR = 0x01
    ADMINISTRATOR = 0xff
    PERMISSION_MAP = {
        OPERATOR : ('operator',u'操作员权限'),
        ADMINISTRATOR: ('administrator',u'至高无上的权限'),
    }

# 用户-角色多对多的关系表
user_role = db.Table('cms_user_role',
        db.Column('user_id',db.String(30),db.ForeignKey('cms_user.id')),
        db.Column('role_id',db.Integer,db.ForeignKey('cms_role.id')))

# CMS用户表
class CMSUser(db.Model,BaseModel):
    __tablename__ = 'cms_user'
    id = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    _password = db.Column(db.String(200), nullable=False)
    joined_time = db.Column(db.DateTime,default=datetime.now())
    is_active = db.Column(db.Boolean,default=True)
    last_login_time = db.Column(db.DateTime,nullable=True)
    roles = db.relationship('CMSRole',secondary=user_role,backref='users')

    def __init__(self, username, email, password):
        self.id = shortuuid.uuid()
        self.username = username
        self.email = email
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, password):
        result = check_password_hash(self.password, password)
        return result

    def has_permission(self,permission):
        if self.roles is None:
            return False
        all_permissions = reduce(or_,map(lambda x: x.permissions,self.roles))
        return all_permissions & permission == permission

    @property
    def is_superadmin(self):
        return self.has_permission(CMSPermission.ADMINISTRATOR)

    @property
    def permissions(self):
        if self.roles is None:
            return None
        permissions = reduce(or_,map(lambda x: x.permissions,self.roles))
        permission_dicts = []
        for key,value in CMSPermission.PERMISSION_MAP.items():
            if key & permissions:
                permission_dicts.append({key:value})
        return permission_dicts



# CMS角色表
class CMSRole(db.Model,BaseModel):
    __tablename__ = 'cms_role'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    create_time = db.Column(db.DateTime,default=datetime.now())
    desc = db.Column(db.String(100))
    permissions = db.Column(db.Integer,default=CMSPermission.OPERATOR)

    def __init__(self,name,desc=None):
        self.name = name
        self.desc = desc