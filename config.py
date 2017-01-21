#coding: utf8
import os

SECRET_KEY = os.urandom(24)

DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'tzbbs_v2'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

SERVER_NAME = 'www.tzpython.com'


# 邮箱的配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USERNAME = '2413357360@qq.com'
MAIL_PASSWORD = 'kswaqavhlfmldjdh'
MAIL_DEFAULT_SENDER = '2413357360@qq.com'
MAIL_USE_TLS = True