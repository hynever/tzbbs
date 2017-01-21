#coding: utf8

# 自定义的setting配置文件

#memcached
MEMCACHED_HOST = '127.0.0.1'
MEMCACHED_PORT = '11211'
MEMCACHED_URI = MEMCACHED_HOST+':'+MEMCACHED_PORT

# 邮箱配置


# session的用户id名称
SESSION_FRONT_USER_ID = 'frontuserid'
SESSION_CMS_USER_ID = 'cmsuserid'

PAGE_NUM = 15


# 登录一次加2个积分
LOGIN_UP_POINTS = 2

# 评论加一个积分
COMMENT_UP_POINTS = 1

# 评论必须要有的积分
COMMENT_ALLOW_POINTS = 5

# 发布帖子必须要有的积分
POST_ALLOW_POINTS = 10