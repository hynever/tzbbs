# coding: utf8

# 存放所有的枚举类型


class PostSortType(object):
    """
        帖子排序类型
    """
    TIME = 1 # 按时间排序
    HIGHLIGHT = 2 # 按加精
    READEDCOUNT = 3 # 按阅读量
    COMMENT_COUNT = 4 # 评论数
    STAR_COUNT = 5 # 点赞数