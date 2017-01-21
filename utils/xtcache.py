#coding: utf8

#使用memcached
from settings import MEMCACHED_URI
import memcache
cache = memcache.Client([MEMCACHED_URI],debug=True)

# 从缓存中获取数据的函数
def get(key=None):
    if key:
        return cache.get(key)
    return None

# 设置缓存的函数，默认过期时间是5分钟
def set(key=None,value=None,timeout=5*60):
    if key and value:
        result = cache.set(key,value,timeout)
        return result
    return False

# 删除缓存
def delete(key=None):
    if key:
        cache.delete(key)
        return True
    return False