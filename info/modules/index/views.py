# 主页的逻辑

from . import index_blue
from info import redis_store

@index_blue.route('/')
def index():
    # 测试redis 数据库
    redis_store.set('name', 'xxx')
    return 'index'