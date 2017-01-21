#coding: utf8
import flask
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
import config
from exts import db
from models.common import basemodels,postmodels
from models.front import accountmodels as front_accountmodels
from models.cms import accountmodels as cms_accountmodels

app = flask.Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 创建命令管理器
manager = Manager(app)

#绑定app到db
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

CMSRole = cms_accountmodels.CMSRole
CMSUser = cms_accountmodels.CMSUser
FrontUser = front_accountmodels.FrontUser
FrontRole = front_accountmodels.FrontRole

# 创建超级用户的命令
@manager.option('-e','--email',dest='email')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-r','--role',dest='role')
def create_superuser(email,username,password,role):
    try:
        roleModel = CMSRole.query.filter_by(name=role.decode('gbk'.encode('utf8'))).first()
        if roleModel:
            user = CMSUser(username=username.decode('gbk').encode('utf8'),email=email,password=password)
            user.roles.append(roleModel)
            db.session.add(user)
            db.session.commit()
            print u'恭喜！超级管理员添加成功！'
        else:
            print u'没有%s这个角色' % role
    except Exception,e:
        print u'错误：',e


# 创建CMS角色
@manager.option('-n','--name',dest='name')
def create_role(name):
    try:
        role = CMSRole(name=name.decode('gbk').encode('utf8'))
        db.session.add(role)
        db.session.commit()
        print u'恭喜！角色添加成功！'
    except Exception,e:
        print u'错误：',e


# 创建前端的角色
@manager.option('-n','--name',dest='name')
def create_front_role(name):
    try:
        role = FrontRole(name=name.decode('gbk').encode('utf8'))
        db.session.add(role)
        db.session.commit()
        print u'恭喜！角色添加成功！'
    except Exception,e:
        print u'错误：',e


@manager.option('-e','--email',dest='email')
@manager.option('-p','--password',dest='password')
def update_pwd(email,password):
    try:
        user = CMSUser.query.filter_by(email=email).first()
        if user:
            user.password = password
            db.session.commit()
            print u'恭喜！密码修改成功！'
        else:
            print u'该邮箱不存在！'
    except Exception,e:
        print u'错误：',e



if __name__ == '__main__':
    manager.run()